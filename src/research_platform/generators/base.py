"""Base generator interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseGenerator(ABC):
    """Abstract base class for content generators."""

    @abstractmethod
    async def generate(self, data: dict[str, Any], output_path: Path) -> Path:
        """
        Generate content from data.

        Args:
            data: Input data
            output_path: Where to save generated content

        Returns:
            Path to generated file
        """
        pass

    @abstractmethod
    async def validate_output(self, output_path: Path) -> bool:
        """Validate generated output."""
        pass
