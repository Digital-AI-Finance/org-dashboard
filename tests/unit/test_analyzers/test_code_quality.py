"""Tests for CodeQualityAnalyzer."""

import logging
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from research_platform.analyzers.code_quality import CodeQualityAnalyzer
from research_platform.models.repository import Repository


@pytest.fixture
def code_quality_analyzer():
    """Create CodeQualityAnalyzer instance."""
    return CodeQualityAnalyzer()


@pytest.fixture
def code_quality_analyzer_with_logger():
    """Create CodeQualityAnalyzer with custom logger."""
    logger = logging.getLogger("test_code_quality")
    return CodeQualityAnalyzer(logger=logger)


class TestCodeQualityAnalyzer:
    """Tests for CodeQualityAnalyzer functionality."""

    @pytest.mark.asyncio
    async def test_analyze_returns_quality_scores(self, code_quality_analyzer, sample_repositories):
        """Test that analyze returns quality scores for repositories."""
        result = await code_quality_analyzer.analyze(sample_repositories)

        assert "timestamp" in result
        assert "total_repos" in result
        assert "analyzed" in result
        assert "scores" in result
        assert result["total_repos"] == len(sample_repositories)

    @pytest.mark.asyncio
    async def test_analyze_empty_list(self, code_quality_analyzer):
        """Test analyzing empty repository list."""
        result = await code_quality_analyzer.analyze([])

        assert result["total_repos"] == 0
        assert result["analyzed"] == 0
        assert result["scores"] == {}

    @pytest.mark.asyncio
    async def test_analyze_single_repository(self, code_quality_analyzer, sample_repository):
        """Test analyzing a single repository."""
        result = await code_quality_analyzer.analyze([sample_repository])

        assert result["total_repos"] == 1
        assert result["analyzed"] == 1
        assert sample_repository.name in result["scores"]

    @pytest.mark.asyncio
    async def test_score_structure(self, code_quality_analyzer, sample_repository):
        """Test the structure of individual repository scores."""
        result = await code_quality_analyzer.analyze([sample_repository])
        repo_score = result["scores"][sample_repository.name]

        assert "overall_score" in repo_score
        assert "activity_score" in repo_score
        assert "community_score" in repo_score
        assert "documentation_score" in repo_score
        assert "code_quality_score" in repo_score

    @pytest.mark.asyncio
    async def test_analyze_handles_errors(self, code_quality_analyzer):
        """Test that analysis errors are handled gracefully."""
        bad_repo = MagicMock(spec=Repository)
        bad_repo.name = "bad-repo"
        bad_repo.calculate_health_score.side_effect = Exception("Analysis failed")

        result = await code_quality_analyzer.analyze([bad_repo])

        assert result["total_repos"] == 1
        assert result["analyzed"] == 0

    @pytest.mark.asyncio
    async def test_validate_results_valid(self, code_quality_analyzer, sample_repositories):
        """Test validate_results returns True for valid results."""
        result = await code_quality_analyzer.analyze(sample_repositories)
        assert await code_quality_analyzer.validate_results(result) is True

    @pytest.mark.asyncio
    async def test_validate_results_missing_timestamp(self, code_quality_analyzer):
        """Test validate_results returns False when timestamp missing."""
        invalid_result = {"scores": {"repo": {}}}
        assert await code_quality_analyzer.validate_results(invalid_result) is False

    @pytest.mark.asyncio
    async def test_validate_results_missing_scores(self, code_quality_analyzer):
        """Test validate_results returns False when scores missing."""
        invalid_result = {"timestamp": datetime.now().isoformat()}
        assert await code_quality_analyzer.validate_results(invalid_result) is False

    @pytest.mark.asyncio
    async def test_concurrent_analysis(self, code_quality_analyzer, sample_repositories):
        """Test that analysis runs concurrently."""
        # All repos should be analyzed even with many repos
        result = await code_quality_analyzer.analyze(sample_repositories)
        assert result["analyzed"] == len(sample_repositories)

    @pytest.mark.asyncio
    async def test_uses_custom_logger(self, code_quality_analyzer_with_logger):
        """Test that custom logger is used for warnings."""
        bad_repo = MagicMock(spec=Repository)
        bad_repo.name = "fail-repo"
        bad_repo.calculate_health_score.side_effect = ValueError("Test error")

        with patch.object(code_quality_analyzer_with_logger.logger, "warning") as mock_warn:
            await code_quality_analyzer_with_logger.analyze([bad_repo])
            mock_warn.assert_called_once()
