"""Unit tests for the pipeline orchestrator."""

import asyncio

import pytest

from research_platform.core.orchestrator import PipelineOrchestrator, PipelineResult
from research_platform.core.phase import Phase, PhaseConfig


class MockSuccessPhase(Phase):
    """Mock phase that always succeeds."""

    async def execute(self, context):
        return {"success": True, "data": "test"}

    def validate_input(self, context):
        return True


class MockFailurePhase(Phase):
    """Mock phase that always fails."""

    async def execute(self, context):
        raise Exception("Intentional failure")

    def validate_input(self, context):
        return True


class MockValidationFailPhase(Phase):
    """Mock phase that fails validation."""

    async def execute(self, context):
        return {"data": "should not reach here"}

    def validate_input(self, context):
        return False


class TestPipelineOrchestrator:
    """Test suite for PipelineOrchestrator."""

    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator instance."""
        config = {"critical_phases": ["fetch_data"], "clear_context_on_cleanup": False}
        return PipelineOrchestrator(config)

    @pytest.fixture
    def success_phase(self):
        """Create a successful phase."""
        config = PhaseConfig(name="success_phase", timeout=5)
        return MockSuccessPhase(config)

    @pytest.fixture
    def failure_phase(self):
        """Create a failing phase."""
        config = PhaseConfig(name="failure_phase", timeout=5, retry_count=1)
        return MockFailurePhase(config)

    @pytest.mark.asyncio
    async def test_register_phase(self, orchestrator, success_phase):
        """Test registering a phase."""
        orchestrator.register_phase(success_phase)

        assert len(orchestrator.phases) == 1
        assert orchestrator.phases[0] == success_phase

    @pytest.mark.asyncio
    async def test_register_multiple_phases(self, orchestrator, success_phase, failure_phase):
        """Test registering multiple phases."""
        orchestrator.register_phases([success_phase, failure_phase])

        assert len(orchestrator.phases) == 2

    @pytest.mark.asyncio
    async def test_successful_pipeline_execution(self, orchestrator, success_phase):
        """Test successful pipeline execution."""
        orchestrator.register_phase(success_phase)

        result = await orchestrator.execute_pipeline()

        assert result.success is True
        assert "success_phase" in result.phases_completed
        assert len(result.phases_failed) == 0
        assert "success" in result.data
        assert result.data["success"] is True

    @pytest.mark.asyncio
    async def test_failed_pipeline_execution(self, orchestrator, failure_phase):
        """Test pipeline execution with failure."""
        orchestrator.register_phase(failure_phase)

        result = await orchestrator.execute_pipeline()

        assert result.success is False
        assert "failure_phase" in result.phases_failed
        assert len(result.phases_completed) == 0
        assert "failure_phase" in result.errors

    @pytest.mark.asyncio
    async def test_mixed_pipeline_execution(self, orchestrator, success_phase, failure_phase):
        """Test pipeline with both successful and failing phases."""
        # Configure failure phase as non-critical
        failure_phase.config.name = "optional_phase"

        orchestrator.register_phases([success_phase, failure_phase])

        result = await orchestrator.execute_pipeline()

        assert result.success is False  # Overall failure due to error
        assert "success_phase" in result.phases_completed
        assert "optional_phase" in result.phases_failed

    @pytest.mark.asyncio
    async def test_validation_failure(self, orchestrator):
        """Test phase validation failure."""
        config = PhaseConfig(name="validation_fail")
        phase = MockValidationFailPhase(config)

        orchestrator.register_phase(phase)

        result = await orchestrator.execute_pipeline()

        assert result.success is False
        assert "validation_fail" in result.phases_failed

    @pytest.mark.asyncio
    async def test_disabled_phase_skipped(self, orchestrator, success_phase):
        """Test that disabled phases are skipped."""
        success_phase.config.enabled = False

        orchestrator.register_phase(success_phase)

        result = await orchestrator.execute_pipeline()

        assert result.success is True
        assert len(result.phases_completed) == 0
        assert len(result.phases_failed) == 0

    @pytest.mark.asyncio
    async def test_phase_timeout(self, orchestrator):
        """Test phase timeout handling."""

        class SlowPhase(Phase):
            async def execute(self, context):
                await asyncio.sleep(10)  # Longer than timeout
                return {"data": "too late"}

            def validate_input(self, context):
                return True

        config = PhaseConfig(name="slow_phase", timeout=0.1, retry_count=1)
        phase = SlowPhase(config)

        orchestrator.register_phase(phase)

        result = await orchestrator.execute_pipeline()

        assert result.success is False
        assert "slow_phase" in result.phases_failed
        assert "timed out" in result.errors["slow_phase"].lower()

    @pytest.mark.asyncio
    async def test_retry_mechanism(self, orchestrator):
        """Test phase retry on failure."""
        attempt_count = 0

        class RetryPhase(Phase):
            async def execute(self, context):
                nonlocal attempt_count
                attempt_count += 1
                if attempt_count < 2:
                    raise Exception("First attempt fails")
                return {"attempts": attempt_count}

            def validate_input(self, context):
                return True

        config = PhaseConfig(name="retry_phase", retry_count=3)
        phase = RetryPhase(config)

        orchestrator.register_phase(phase)

        result = await orchestrator.execute_pipeline()

        assert result.success is True
        assert "retry_phase" in result.phases_completed
        assert result.data["attempts"] == 2

    @pytest.mark.asyncio
    async def test_critical_phase_stops_pipeline(self, orchestrator, failure_phase, success_phase):
        """Test that critical phase failure stops the pipeline."""
        # Make failure phase critical
        failure_phase.config.name = "fetch_data"  # This is in critical_phases

        orchestrator.register_phases([failure_phase, success_phase])

        result = await orchestrator.execute_pipeline()

        assert result.success is False
        assert "fetch_data" in result.phases_failed
        assert "success_phase" not in result.phases_completed  # Should not run

    @pytest.mark.asyncio
    async def test_context_propagation(self, orchestrator):
        """Test context propagation between phases."""

        class Phase1(Phase):
            async def execute(self, context):
                return {"phase1_data": "value1"}

            def validate_input(self, context):
                return True

        class Phase2(Phase):
            async def execute(self, context):
                assert "phase1_data" in context
                return {"phase2_data": context["phase1_data"] + "_modified"}

            def validate_input(self, context):
                return "phase1_data" in context

        config1 = PhaseConfig(name="phase1")
        config2 = PhaseConfig(name="phase2", dependencies=["phase1_data"])

        phase1 = Phase1(config1)
        phase2 = Phase2(config2)

        orchestrator.register_phases([phase1, phase2])

        result = await orchestrator.execute_pipeline()

        assert result.success is True
        assert result.data["phase1_data"] == "value1"
        assert result.data["phase2_data"] == "value1_modified"

    @pytest.mark.asyncio
    async def test_initial_context(self, orchestrator, success_phase):
        """Test providing initial context to pipeline."""
        initial_context = {"initial_key": "initial_value"}

        orchestrator.register_phase(success_phase)

        result = await orchestrator.execute_pipeline(initial_context)

        assert "initial_key" in result.data
        assert result.data["initial_key"] == "initial_value"

    @pytest.mark.asyncio
    async def test_get_phase_result(self, orchestrator, success_phase):
        """Test retrieving phase results."""
        orchestrator.register_phase(success_phase)

        await orchestrator.execute_pipeline()

        phase_result = orchestrator.get_phase_result("success_phase")

        assert phase_result is not None
        assert phase_result.success is True
        assert phase_result.phase_name == "success_phase"

    @pytest.mark.asyncio
    async def test_get_context_data(self, orchestrator, success_phase):
        """Test retrieving context data."""
        orchestrator.register_phase(success_phase)

        await orchestrator.execute_pipeline()

        data = orchestrator.get_context_data("success")

        assert data is True

    @pytest.mark.asyncio
    async def test_cleanup(self, orchestrator, success_phase):
        """Test cleanup after pipeline execution."""
        orchestrator.register_phase(success_phase)

        await orchestrator.execute_pipeline()

        # Verify data exists
        assert len(orchestrator._phase_results) > 0

        await orchestrator.cleanup()

        # Verify cleanup
        assert len(orchestrator._phase_results) == 0

    def test_validate_pipeline_config(self, orchestrator):
        """Test pipeline configuration validation."""

        class PhaseWithDep(Phase):
            async def execute(self, context):
                return {}

            def validate_input(self, context):
                return True

        # Valid configuration
        config = PhaseConfig(name="phase1", dependencies=[])
        phase = PhaseWithDep(config)
        orchestrator.register_phase(phase)

        assert orchestrator.validate_pipeline_config() is True

        # Invalid configuration - unknown dependency
        config2 = PhaseConfig(name="phase2", dependencies=["unknown_phase"])
        phase2 = PhaseWithDep(config2)
        orchestrator.register_phase(phase2)

        assert orchestrator.validate_pipeline_config() is False

    def test_get_execution_plan(self, orchestrator, success_phase, failure_phase):
        """Test getting the execution plan."""
        orchestrator.register_phases([success_phase, failure_phase])

        plan = orchestrator.get_execution_plan()

        assert len(plan) == 2
        assert plan[0]["name"] == "success_phase"
        assert plan[1]["name"] == "failure_phase"
        assert "timeout" in plan[0]
        assert "retry_count" in plan[0]

    def test_pipeline_result_to_dict(self):
        """Test PipelineResult serialization."""
        result = PipelineResult(
            success=True,
            phases_completed=["phase1", "phase2"],
            phases_failed=[],
            errors={},
            warnings={"phase1": ["warning1"]},
            data={"key": "value"},
            duration=10.5,
        )

        data = result.to_dict()

        assert data["success"] is True
        assert data["phases_completed"] == ["phase1", "phase2"]
        assert data["duration"] == 10.5
        assert "summary" in data
        assert data["summary"]["successful"] == 2
