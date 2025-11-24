"""Tests for MarkdownGenerator."""

import logging
from unittest.mock import patch

import pytest
from jinja2 import TemplateNotFound

from research_platform.generators.markdown import MarkdownGenerator


@pytest.fixture
def template_dir(temp_dir):
    """Create a template directory with test templates."""
    templates = temp_dir / "templates"
    templates.mkdir(exist_ok=True)

    # Create a simple test template
    test_template = templates / "test.md.j2"
    test_template.write_text(
        """# {{ title }}

{{ content }}

Generated: {{ generated_at | format_date }}
Count: {{ count | format_number }}
"""
    )

    # Create index template
    index_template = templates / "index.md.j2"
    index_template.write_text("# Index\n\n{{ description }}")

    return templates


@pytest.fixture
def markdown_generator(template_dir):
    """Create MarkdownGenerator instance."""
    return MarkdownGenerator(template_dir)


@pytest.fixture
def markdown_generator_with_logger(template_dir):
    """Create MarkdownGenerator with custom logger."""
    logger = logging.getLogger("test_markdown")
    return MarkdownGenerator(template_dir, logger=logger)


class TestMarkdownGenerator:
    """Tests for MarkdownGenerator functionality."""

    @pytest.mark.asyncio
    async def test_generate_basic_template(self, markdown_generator, temp_dir):
        """Test generating a basic markdown file."""
        output_path = temp_dir / "output" / "test.md"

        data = {
            "template": "test.md.j2",
            "title": "Test Title",
            "content": "This is test content.",
            "generated_at": "2024-01-15T10:30:00",
            "count": 12345,
        }

        result = await markdown_generator.generate(data, output_path)

        assert result == output_path
        assert output_path.exists()

        content = output_path.read_text()
        assert "# Test Title" in content
        assert "This is test content." in content

    @pytest.mark.asyncio
    async def test_generate_creates_output_directory(self, markdown_generator, temp_dir):
        """Test that generate creates the output directory if needed."""
        output_path = temp_dir / "nested" / "deep" / "output.md"

        data = {"template": "index.md.j2", "description": "Test"}

        await markdown_generator.generate(data, output_path)

        assert output_path.parent.exists()
        assert output_path.exists()

    @pytest.mark.asyncio
    async def test_generate_with_default_template(self, markdown_generator, temp_dir):
        """Test using default template when not specified."""
        output_path = temp_dir / "default.md"

        data = {"description": "Default template test"}

        await markdown_generator.generate(data, output_path)

        content = output_path.read_text()
        assert "Index" in content
        assert "Default template test" in content

    @pytest.mark.asyncio
    async def test_generate_missing_template_raises_error(self, markdown_generator, temp_dir):
        """Test that missing template raises an error."""
        output_path = temp_dir / "error.md"

        data = {"template": "nonexistent.md.j2"}

        with pytest.raises(TemplateNotFound):
            await markdown_generator.generate(data, output_path)

    @pytest.mark.asyncio
    async def test_validate_output_existing_file(self, markdown_generator, temp_dir):
        """Test validate_output returns True for existing non-empty file."""
        output_path = temp_dir / "valid.md"
        output_path.write_text("# Valid Content\n")

        result = await markdown_generator.validate_output(output_path)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_output_nonexistent_file(self, markdown_generator, temp_dir):
        """Test validate_output returns False for nonexistent file."""
        output_path = temp_dir / "nonexistent.md"

        result = await markdown_generator.validate_output(output_path)
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_output_empty_file(self, markdown_generator, temp_dir):
        """Test validate_output returns False for empty file."""
        output_path = temp_dir / "empty.md"
        output_path.write_text("")

        result = await markdown_generator.validate_output(output_path)
        assert result is False

    def test_format_date_filter_valid(self, markdown_generator):
        """Test format_date filter with valid ISO date."""
        result = MarkdownGenerator._format_date("2024-01-15T10:30:00")
        assert result == "2024-01-15"

    def test_format_date_filter_with_timezone(self, markdown_generator):
        """Test format_date filter with timezone."""
        result = MarkdownGenerator._format_date("2024-01-15T10:30:00Z")
        assert result == "2024-01-15"

    def test_format_date_filter_invalid(self, markdown_generator):
        """Test format_date filter with invalid date returns original."""
        result = MarkdownGenerator._format_date("not-a-date")
        assert result == "not-a-date"

    def test_format_number_filter(self, markdown_generator):
        """Test format_number filter."""
        assert MarkdownGenerator._format_number(1000) == "1,000"
        assert MarkdownGenerator._format_number(1234567) == "1,234,567"
        assert MarkdownGenerator._format_number(0) == "0"
        assert MarkdownGenerator._format_number(999.5) == "1,000"

    def test_custom_filters_registered(self, markdown_generator):
        """Test that custom filters are registered in environment."""
        assert "format_date" in markdown_generator.env.filters
        assert "format_number" in markdown_generator.env.filters

    @pytest.mark.asyncio
    async def test_uses_custom_logger(self, markdown_generator_with_logger, temp_dir):
        """Test that custom logger is used."""
        output_path = temp_dir / "logged.md"
        data = {"template": "index.md.j2", "description": "Test"}

        with patch.object(markdown_generator_with_logger.logger, "info") as mock_info:
            await markdown_generator_with_logger.generate(data, output_path)
            mock_info.assert_called_once()
