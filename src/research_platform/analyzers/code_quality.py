"""Code quality analyzer."""

import asyncio
import logging
from datetime import datetime
from typing import Any

from ..models.repository import Repository
from .base import BaseAnalyzer


class CodeQualityAnalyzer(BaseAnalyzer):
    """Analyze code quality metrics for repositories."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)

    async def analyze(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Analyze code quality for all repositories.

        Args:
            repositories: List of repositories

        Returns:
            Code quality report
        """
        tasks = [self._analyze_repo(repo) for repo in repositories]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        quality_scores = {}
        for repo, result in zip(repositories, results):
            if isinstance(result, Exception):
                self.logger.warning(f"Failed to analyze {repo.name}: {result}")
                continue
            quality_scores[repo.name] = result

        return {
            "timestamp": datetime.now().isoformat(),
            "total_repos": len(repositories),
            "analyzed": len(quality_scores),
            "scores": quality_scores,
        }

    async def _analyze_repo(self, repo: Repository) -> dict[str, Any]:
        """Analyze a single repository."""
        # Use existing repo health score as proxy
        quality_score = repo.calculate_health_score()

        return {
            "overall_score": quality_score["overall"],
            "activity_score": quality_score["scores"]["activity"],
            "community_score": quality_score["scores"]["community"],
            "documentation_score": quality_score["scores"]["documentation"],
            "code_quality_score": quality_score["scores"]["code_quality"],
        }

    async def validate_results(self, results: dict[str, Any]) -> bool:
        """Validate analysis results."""
        required = ["timestamp", "scores"]
        return all(key in results for key in required)


