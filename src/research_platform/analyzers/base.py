"""Base analyzer interface."""

from abc import ABC, abstractmethod
from typing import Any

from ..models.repository import Repository


class BaseAnalyzer(ABC):
    """Abstract base class for repository analyzers."""

    @abstractmethod
    async def analyze(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Analyze repositories and return results.

        Args:
            repositories: List of repositories to analyze

        Returns:
            Analysis results as dictionary
        """
        pass

    @abstractmethod
    async def validate_results(self, results: dict[str, Any]) -> bool:
        """Validate analysis results."""
        pass
