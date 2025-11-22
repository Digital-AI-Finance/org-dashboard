"""Repository health scoring."""

import logging
from datetime import datetime
from typing import Any

from ..models.repository import Repository
from .base import BaseAnalyzer


class HealthScorer(BaseAnalyzer):
    """Calculate multi-dimensional health scores for repositories."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)

    async def analyze(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Calculate health scores for all repositories.

        Args:
            repositories: List of repositories

        Returns:
            Health report with scores
        """
        health_scores = {}

        for repo in repositories:
            try:
                health_scores[repo.name] = repo.calculate_health_score()
            except Exception as e:
                self.logger.warning(f"Failed to score {repo.name}: {e}")
                continue

        return {
            "timestamp": datetime.now().isoformat(),
            "total_repos": len(repositories),
            "scored": len(health_scores),
            "scores": health_scores,
        }

    async def validate_results(self, results: dict[str, Any]) -> bool:
        """Validate health scoring results."""
        return "scores" in results and len(results["scores"]) > 0
