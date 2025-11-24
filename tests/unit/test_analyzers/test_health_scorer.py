"""Tests for HealthScorer analyzer."""

import logging
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from research_platform.analyzers.health_scorer import HealthScorer
from research_platform.models.repository import Repository


@pytest.fixture
def health_scorer():
    """Create HealthScorer instance."""
    return HealthScorer()


@pytest.fixture
def health_scorer_with_logger():
    """Create HealthScorer with custom logger."""
    logger = logging.getLogger("test_health")
    return HealthScorer(logger=logger)


class TestHealthScorer:
    """Tests for HealthScorer functionality."""

    @pytest.mark.asyncio
    async def test_analyze_returns_health_scores(self, health_scorer, sample_repositories):
        """Test that analyze returns health scores for repositories."""
        result = await health_scorer.analyze(sample_repositories)

        assert "timestamp" in result
        assert "total_repos" in result
        assert "scored" in result
        assert "scores" in result
        assert result["total_repos"] == len(sample_repositories)

    @pytest.mark.asyncio
    async def test_analyze_empty_list(self, health_scorer):
        """Test analyzing empty repository list."""
        result = await health_scorer.analyze([])

        assert result["total_repos"] == 0
        assert result["scored"] == 0
        assert result["scores"] == {}

    @pytest.mark.asyncio
    async def test_analyze_single_repository(self, health_scorer, sample_repository):
        """Test analyzing a single repository."""
        result = await health_scorer.analyze([sample_repository])

        assert result["total_repos"] == 1
        assert result["scored"] == 1
        assert sample_repository.name in result["scores"]

    @pytest.mark.asyncio
    async def test_analyze_handles_scoring_errors(self, health_scorer):
        """Test that scoring errors are handled gracefully."""
        # Create a repo that will fail scoring
        bad_repo = MagicMock(spec=Repository)
        bad_repo.name = "bad-repo"
        bad_repo.calculate_health_score.side_effect = Exception("Score calculation failed")

        result = await health_scorer.analyze([bad_repo])

        assert result["total_repos"] == 1
        assert result["scored"] == 0

    @pytest.mark.asyncio
    async def test_validate_results_valid(self, health_scorer, sample_repositories):
        """Test validate_results returns True for valid results."""
        result = await health_scorer.analyze(sample_repositories)
        assert await health_scorer.validate_results(result) is True

    @pytest.mark.asyncio
    async def test_validate_results_invalid_missing_scores(self, health_scorer):
        """Test validate_results returns False when scores missing."""
        invalid_result = {"timestamp": datetime.now().isoformat()}
        assert await health_scorer.validate_results(invalid_result) is False

    @pytest.mark.asyncio
    async def test_validate_results_invalid_empty_scores(self, health_scorer):
        """Test validate_results returns False for empty scores."""
        invalid_result = {"scores": {}}
        assert await health_scorer.validate_results(invalid_result) is False

    @pytest.mark.asyncio
    async def test_timestamp_format(self, health_scorer, sample_repository):
        """Test that timestamp is in ISO format."""
        result = await health_scorer.analyze([sample_repository])
        # Should not raise
        datetime.fromisoformat(result["timestamp"])

    @pytest.mark.asyncio
    async def test_uses_custom_logger(self, health_scorer_with_logger):
        """Test that custom logger is used."""
        bad_repo = MagicMock(spec=Repository)
        bad_repo.name = "fail-repo"
        bad_repo.calculate_health_score.side_effect = ValueError("Test error")

        with patch.object(health_scorer_with_logger.logger, "warning") as mock_warn:
            await health_scorer_with_logger.analyze([bad_repo])
            mock_warn.assert_called_once()
