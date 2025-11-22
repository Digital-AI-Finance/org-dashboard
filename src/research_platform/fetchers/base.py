"""Base fetcher interface."""

from abc import ABC, abstractmethod
from typing import Any


class BaseFetcher(ABC):
    """Abstract base class for data fetchers."""

    @abstractmethod
    async def fetch(self, **kwargs: Any) -> dict[str, Any]:
        """Fetch data from source."""
        pass

    @abstractmethod
    async def validate(self, data: dict[str, Any]) -> bool:
        """Validate fetched data."""
        pass
