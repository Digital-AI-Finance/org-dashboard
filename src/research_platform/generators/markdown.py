"""Markdown page generator using Jinja2 templates."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles
from jinja2 import Environment, FileSystemLoader

from .base import BaseGenerator


class MarkdownGenerator(BaseGenerator):
    """Generate markdown pages from Jinja2 templates."""

    def __init__(
        self,
        template_dir: Path,
        logger: logging.Logger | None = None,
    ):
        self.template_dir = template_dir
        self.logger = logger or logging.getLogger(__name__)
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

        # Add custom filters
        self.env.filters["format_date"] = self._format_date
        self.env.filters["format_number"] = self._format_number

    async def generate(self, data: dict[str, Any], output_path: Path) -> Path:
        """
        Generate markdown from template.

        Args:
            data: Template context data including 'template' key
            output_path: Output file path

        Returns:
            Path to generated file
        """
        template_name = data.get("template", "index.md.j2")

        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**data)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file asynchronously
            async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                await f.write(rendered)

            self.logger.info(f"Generated: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate {output_path}: {e}")
            raise

    async def validate_output(self, output_path: Path) -> bool:
        """Validate generated markdown file."""
        if not output_path.exists():
            return False

        # Check file is not empty
        return output_path.stat().st_size > 0

    @staticmethod
    def _format_date(date_str: str) -> str:
        """Format ISO date string."""
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
        except Exception:
            return date_str

    @staticmethod
    def _format_number(num: float) -> str:
        """Format number with commas."""
        return f"{num:,.0f}"
