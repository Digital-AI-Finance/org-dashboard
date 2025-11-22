"""
GitHub Research Platform
========================

A comprehensive platform for analyzing GitHub organizations with focus on
research repositories, academic citations, and collaboration networks.

Quick Start
-----------
    from research_platform import PlatformBuilder

    builder = PlatformBuilder.from_config("configs/production.yaml")
    result = await builder.build()

Main Components
--------------
- Fetchers: Data collection from GitHub and academic sources
- Analyzers: Code quality, collaboration networks, ML topic modeling
- Generators: Markdown, visualizations, search indices
- Core: Pipeline orchestration, configuration, error handling

For more information, see the documentation at:
https://github.com/Digital-AI-Finance/GithubQuantlet
"""

__version__ = "2.0.0"
__author__ = "Digital AI Finance Research"

from .config.settings import Settings
from .core.orchestrator import PipelineOrchestrator
from .models.repository import Repository

__all__ = ["PipelineOrchestrator", "Settings", "Repository"]
