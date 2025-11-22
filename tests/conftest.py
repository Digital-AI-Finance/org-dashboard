"""Pytest configuration and fixtures for the research platform tests."""

import asyncio
import shutil

# Add src to path for imports
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_platform.config.settings import GitHubConfig, Settings
from research_platform.models.repository import Repository


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_settings(temp_dir):
    """Create test settings."""
    return Settings(
        app_name="Test Platform",
        environment="testing",
        debug=True,
        output_directory=temp_dir / "output",
        data_directory=temp_dir / "data",
        template_directory=Path("templates"),  # Assuming templates exist
        github=GitHubConfig(token="test-token", organization="test-org"),
    )


@pytest.fixture
def mock_github_client():
    """Create a mock GitHub client."""
    client = Mock()
    client.get_user.return_value.login = "test-user"
    client.get_rate_limit.return_value.core.remaining = 5000
    return client


@pytest.fixture
def sample_repository():
    """Create a sample repository for testing."""
    return Repository(
        id=123456,
        name="test-repo",
        full_name="test-org/test-repo",
        description="A test repository for unit tests",
        language="Python",
        stars=42,
        forks=10,
        open_issues=3,
        created_at=datetime(2023, 1, 1),
        updated_at=datetime(2024, 1, 1),
        topics=["testing", "python", "research"],
        contributors_count=5,
    )


@pytest.fixture
def sample_repositories():
    """Create multiple sample repositories."""
    repos = []
    languages = ["Python", "JavaScript", "R", "Julia", None]

    for i in range(10):
        repo = Repository(
            id=100000 + i,
            name=f"repo-{i}",
            full_name=f"test-org/repo-{i}",
            description=f"Test repository number {i}",
            language=languages[i % len(languages)],
            stars=i * 10,
            forks=i * 2,
            open_issues=i,
            created_at=datetime(2023, 1, 1 + i),
            updated_at=datetime(2024, 1, 1 + i),
            topics=[f"topic-{i}", "research"] if i % 2 == 0 else [],
            contributors_count=i + 1,
        )
        repos.append(repo)

    return repos


@pytest.fixture
def mock_github_repo():
    """Create a mock PyGithub repository object."""
    repo = Mock()
    repo.id = 123456
    repo.name = "test-repo"
    repo.full_name = "test-org/test-repo"
    repo.description = "A test repository"
    repo.language = "Python"
    repo.homepage = "https://test.com"
    repo.default_branch = "main"
    repo.stargazers_count = 100
    repo.forks_count = 20
    repo.watchers_count = 50
    repo.open_issues_count = 5
    repo.size = 1024
    repo.created_at = datetime(2023, 1, 1)
    repo.updated_at = datetime(2024, 1, 1)
    repo.pushed_at = datetime(2024, 1, 1)
    repo.has_issues = True
    repo.has_projects = True
    repo.has_wiki = True
    repo.has_pages = False
    repo.has_downloads = True
    repo.archived = False
    repo.disabled = False
    repo.is_template = False
    repo.get_topics.return_value = ["python", "testing"]

    # Mock contributors
    contributor_mock = Mock()
    contributor_mock.totalCount = 10
    repo.get_contributors.return_value = contributor_mock

    return repo


@pytest.fixture
def pipeline_context():
    """Create a sample pipeline context."""
    return {
        "organization": "test-org",
        "repositories": [],
        "stats": {"total_repos": 0, "total_stars": 0, "languages": {}},
        "timestamp": datetime.now().isoformat(),
    }


@pytest.fixture
def mock_phase():
    """Create a mock phase for testing."""
    from research_platform.core.phase import Phase, PhaseConfig

    class MockPhase(Phase):
        async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
            return {"mock_data": "test"}

        def validate_input(self, context: dict[str, Any]) -> bool:
            return True

    config = PhaseConfig(name="mock_phase", enabled=True, timeout=10)

    return MockPhase(config)


@pytest.fixture
def mock_async_response():
    """Create a mock async response."""

    async def async_return(value):
        return value

    return async_return


@pytest.fixture
def sample_config_yaml(temp_dir):
    """Create a sample YAML configuration file."""
    config_content = """
app_name: Test Research Platform
environment: testing
debug: true

github:
  token: test-token
  organization: test-org
  rate_limit_pause: 30
  max_retries: 3

cache:
  enabled: true
  ttl: 1800
  directory: cache
  max_size_mb: 50

logging:
  level: DEBUG
  file: test.log
  console: true

phases:
  fetch_data:
    enabled: true
    timeout: 60
  analyze:
    enabled: true
    timeout: 120

features:
  academic_data: true
  ml_topics: false
"""

    config_path = temp_dir / "test_config.yaml"
    config_path.write_text(config_content)
    return config_path


@pytest.fixture
def mock_api_responses():
    """Mock responses for various API calls."""
    return {
        "repos": [
            {"id": 1, "name": "repo1", "full_name": "org/repo1", "stargazers_count": 10},
            {"id": 2, "name": "repo2", "full_name": "org/repo2", "stargazers_count": 20},
        ],
        "contributors": [
            {"login": "user1", "contributions": 100},
            {"login": "user2", "contributions": 50},
        ],
        "topics": ["machine-learning", "data-science", "python"],
        "languages": {"Python": 50000, "JavaScript": 10000, "HTML": 5000},
    }


# Markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "github_api: mark test as requiring GitHub API")
