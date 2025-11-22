"""Abstract base class for pipeline phases."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging
import asyncio
from datetime import datetime


@dataclass
class PhaseConfig:
    """Configuration for a pipeline phase."""
    name: str
    enabled: bool = True
    timeout: int = 300
    retry_count: int = 3
    cache_ttl: Optional[int] = None
    dependencies: list = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class PhaseResult:
    """Result of phase execution."""

    def __init__(self, phase_name: str):
        self.phase_name = phase_name
        self.start_time = datetime.now()
        self.end_time = None
        self.success = False
        self.data = {}
        self.errors = []
        self.warnings = []

    def complete(self, success: bool, data: Dict[str, Any] = None):
        """Mark phase as complete."""
        self.end_time = datetime.now()
        self.success = success
        if data:
            self.data = data

    @property
    def duration(self) -> float:
        """Get phase execution duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "phase_name": self.phase_name,
            "success": self.success,
            "duration": self.duration,
            "errors": self.errors,
            "warnings": self.warnings,
            "data_keys": list(self.data.keys()) if self.data else []
        }


class Phase(ABC):
    """Abstract base class for pipeline phases."""

    def __init__(self, config: PhaseConfig, logger: logging.Logger = None):
        self.config = config
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self._dependencies = {}
        self._result = None

    def inject_dependency(self, name: str, dependency: Any) -> None:
        """Inject a dependency for this phase."""
        self._dependencies[name] = dependency
        self.logger.debug(f"Injected dependency '{name}' into {self.config.name}")

    def get_dependency(self, name: str) -> Any:
        """Get an injected dependency."""
        if name not in self._dependencies:
            raise ValueError(f"Dependency '{name}' not found in {self.config.name}")
        return self._dependencies[name]

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the phase logic.

        Args:
            context: Shared context containing data from previous phases

        Returns:
            Dictionary of results to be added to context
        """
        pass

    @abstractmethod
    def validate_input(self, context: Dict[str, Any]) -> bool:
        """
        Validate phase input data.

        Args:
            context: Current pipeline context

        Returns:
            True if input is valid, False otherwise
        """
        pass

    def validate_dependencies(self, context: Dict[str, Any]) -> bool:
        """Check if required dependencies are in context."""
        for dep in self.config.dependencies:
            if dep not in context:
                self.logger.error(f"Missing required dependency: {dep}")
                return False
        return True

    async def run(self, context: Dict[str, Any]) -> PhaseResult:
        """Run the phase with error handling and timing."""
        result = PhaseResult(self.config.name)

        try:
            # Validate dependencies
            if not self.validate_dependencies(context):
                result.errors.append("Missing required dependencies")
                result.complete(False)
                return result

            # Validate input
            if not self.validate_input(context):
                result.errors.append("Input validation failed")
                result.complete(False)
                return result

            # Execute phase with timeout
            self.logger.info(f"Starting phase: {self.config.name}")

            phase_data = await asyncio.wait_for(
                self.execute(context),
                timeout=self.config.timeout
            )

            result.complete(True, phase_data)
            self.logger.info(f"Phase {self.config.name} completed successfully in {result.duration:.2f}s")

        except asyncio.TimeoutError:
            error_msg = f"Phase {self.config.name} timed out after {self.config.timeout}s"
            self.logger.error(error_msg)
            result.errors.append(error_msg)
            result.complete(False)

        except Exception as e:
            error_msg = f"Phase {self.config.name} failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            result.errors.append(error_msg)
            result.complete(False)

        self._result = result
        return result

    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle phase execution errors."""
        self.logger.error(f"Phase {self.config.name} error: {error}")
        return {
            "status": "failed",
            "phase": self.config.name,
            "error": str(error)
        }

    def get_result(self) -> Optional[PhaseResult]:
        """Get the last execution result."""
        return self._result