"""Pipeline orchestrator for managing phase execution."""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from .phase import Phase, PhaseResult
from .exceptions import PlatformException


@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    success: bool
    phases_completed: List[str]
    phases_failed: List[str]
    errors: Dict[str, str]
    warnings: Dict[str, List[str]]
    data: Dict[str, Any]
    duration: float
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "phases_completed": self.phases_completed,
            "phases_failed": self.phases_failed,
            "errors": self.errors,
            "warnings": self.warnings,
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
            "summary": {
                "total_phases": len(self.phases_completed) + len(self.phases_failed),
                "successful": len(self.phases_completed),
                "failed": len(self.phases_failed)
            }
        }


class PipelineOrchestrator:
    """Orchestrate pipeline execution with error recovery."""

    def __init__(self, config: Dict[str, Any], logger: logging.Logger = None):
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.phases: List[Phase] = []
        self.context: Dict[str, Any] = {}
        self._phase_results: Dict[str, PhaseResult] = {}

    def register_phase(self, phase: Phase) -> None:
        """Register a phase in the pipeline."""
        self.phases.append(phase)
        self.logger.info(f"Registered phase: {phase.config.name}")

    def register_phases(self, phases: List[Phase]) -> None:
        """Register multiple phases."""
        for phase in phases:
            self.register_phase(phase)

    @asynccontextmanager
    async def _phase_context(self, phase_name: str):
        """Context manager for phase execution."""
        self.logger.info(f"{'=' * 60}")
        self.logger.info(f"Starting phase: {phase_name}")
        self.logger.info(f"{'=' * 60}")

        try:
            yield
        finally:
            self.logger.info(f"Phase {phase_name} completed")

    async def execute_pipeline(self, initial_context: Dict[str, Any] = None) -> PipelineResult:
        """
        Execute all registered phases.

        Args:
            initial_context: Initial context data

        Returns:
            PipelineResult with execution summary
        """
        start_time = asyncio.get_event_loop().time()
        phases_completed = []
        phases_failed = []
        errors = {}
        warnings = {}

        # Initialize context
        self.context = initial_context or {}

        try:
            for phase in self.phases:
                if not phase.config.enabled:
                    self.logger.info(f"Skipping disabled phase: {phase.config.name}")
                    continue

                async with self._phase_context(phase.config.name):
                    # Execute phase
                    result = await self._execute_phase_with_retry(phase)
                    self._phase_results[phase.config.name] = result

                    if result.success:
                        # Update context with phase results
                        if result.data:
                            self.context.update(result.data)
                        phases_completed.append(phase.config.name)

                        # Record warnings
                        if result.warnings:
                            warnings[phase.config.name] = result.warnings

                    else:
                        phases_failed.append(phase.config.name)
                        errors[phase.config.name] = ", ".join(result.errors)

                        # Check if phase failure should stop pipeline
                        if self._should_stop_on_failure(phase):
                            self.logger.error(f"Critical phase {phase.config.name} failed, stopping pipeline")
                            break

        except Exception as e:
            self.logger.error(f"Unexpected pipeline error: {e}", exc_info=True)
            errors["pipeline"] = str(e)

        finally:
            duration = asyncio.get_event_loop().time() - start_time

        return PipelineResult(
            success=len(phases_failed) == 0 and len(errors) == 0,
            phases_completed=phases_completed,
            phases_failed=phases_failed,
            errors=errors,
            warnings=warnings,
            data=self.context,
            duration=duration
        )

    async def _execute_phase_with_retry(self, phase: Phase) -> PhaseResult:
        """Execute a phase with retry logic."""
        last_result = None

        for attempt in range(phase.config.retry_count):
            try:
                result = await phase.run(self.context)

                if result.success:
                    return result

                last_result = result

                # Don't retry if it's a validation error
                if any("validation" in err.lower() for err in result.errors):
                    break

                if attempt < phase.config.retry_count - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(
                        f"Phase {phase.config.name} failed (attempt {attempt + 1}), "
                        f"retrying in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)

            except Exception as e:
                self.logger.error(f"Phase {phase.config.name} exception: {e}")

                if last_result is None:
                    last_result = PhaseResult(phase.config.name)

                last_result.errors.append(str(e))
                last_result.complete(False)

                if attempt == phase.config.retry_count - 1:
                    break

        return last_result

    def _should_stop_on_failure(self, phase: Phase) -> bool:
        """Determine if pipeline should stop on phase failure."""
        # Critical phases that should stop pipeline
        critical_phases = self.config.get("critical_phases", ["fetch_data"])
        return phase.config.name in critical_phases

    def get_phase_result(self, phase_name: str) -> Optional[PhaseResult]:
        """Get result for a specific phase."""
        return self._phase_results.get(phase_name)

    def get_context_data(self, key: str) -> Any:
        """Get data from pipeline context."""
        return self.context.get(key)

    async def cleanup(self):
        """Cleanup resources after pipeline execution."""
        self.logger.info("Cleaning up pipeline resources...")

        # Clear phase results
        self._phase_results.clear()

        # Clear context if configured
        if self.config.get("clear_context_on_cleanup", False):
            self.context.clear()

    def validate_pipeline_config(self) -> bool:
        """Validate pipeline configuration before execution."""
        errors = []

        # Check for circular dependencies
        phase_names = {phase.config.name for phase in self.phases}

        for phase in self.phases:
            for dep in phase.config.dependencies:
                if dep not in phase_names:
                    errors.append(f"Phase {phase.config.name} has unknown dependency: {dep}")

        if errors:
            for error in errors:
                self.logger.error(error)
            return False

        return True

    def get_execution_plan(self) -> List[Dict[str, Any]]:
        """Get the execution plan for the pipeline."""
        plan = []

        for phase in self.phases:
            plan.append({
                "name": phase.config.name,
                "enabled": phase.config.enabled,
                "dependencies": phase.config.dependencies,
                "timeout": phase.config.timeout,
                "retry_count": phase.config.retry_count
            })

        return plan