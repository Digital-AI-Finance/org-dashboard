# GitHub Research Platform - Architecture Recommendations

## 1. Improved Project Structure

Transform from flat scripts to organized package:

```
github_research_platform/
├── src/
│   └── research_platform/
│       ├── __init__.py
│       ├── __main__.py              # Entry point
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py          # Configuration management
│       │   └── constants.py         # Platform constants
│       ├── core/
│       │   ├── __init__.py
│       │   ├── orchestrator.py      # Main pipeline orchestrator
│       │   ├── phase.py             # Phase abstraction
│       │   └── exceptions.py        # Custom exceptions
│       ├── fetchers/
│       │   ├── __init__.py
│       │   ├── base.py              # Abstract fetcher
│       │   ├── github_fetcher.py    # GitHub API operations
│       │   ├── academic_fetcher.py  # Academic data fetching
│       │   └── cache.py             # Caching layer
│       ├── analyzers/
│       │   ├── __init__.py
│       │   ├── base.py              # Abstract analyzer
│       │   ├── code_quality.py     # Code quality analysis
│       │   ├── collaboration.py     # Network analysis
│       │   ├── health_scorer.py     # Repository health
│       │   └── topic_modeling.py    # ML topic extraction
│       ├── generators/
│       │   ├── __init__.py
│       │   ├── base.py              # Abstract generator
│       │   ├── markdown.py          # Markdown generation
│       │   ├── visualizations.py    # Plotly visualizations
│       │   └── search_index.py      # Search indexing
│       ├── models/
│       │   ├── __init__.py
│       │   ├── repository.py        # Repository data model
│       │   ├── citation.py          # Citation model
│       │   └── collaboration.py     # Collaboration model
│       └── utils/
│           ├── __init__.py
│           ├── logger.py            # Logging configuration
│           ├── validators.py        # Data validation
│           └── helpers.py           # Utility functions
├── tests/
│   ├── unit/
│   │   ├── test_fetchers/
│   │   ├── test_analyzers/
│   │   ├── test_generators/
│   │   └── test_models/
│   ├── integration/
│   │   ├── test_pipeline.py
│   │   └── test_github_api.py
│   ├── fixtures/
│   │   ├── sample_repos.json
│   │   └── mock_responses.py
│   └── conftest.py
├── configs/
│   ├── development.yaml
│   ├── production.yaml
│   └── testing.yaml
├── pyproject.toml
├── setup.py
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## 2. Code Architecture Patterns

### A. Dependency Injection & Interfaces

```python
# src/research_platform/core/phase.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

@dataclass
class PhaseConfig:
    """Configuration for a pipeline phase."""
    name: str
    enabled: bool = True
    timeout: int = 300
    retry_count: int = 3
    cache_ttl: Optional[int] = None

class Phase(ABC):
    """Abstract base class for pipeline phases."""

    def __init__(self, config: PhaseConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self._dependencies = {}

    def inject_dependency(self, name: str, dependency: Any) -> None:
        """Inject a dependency for this phase."""
        self._dependencies[name] = dependency

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the phase logic."""
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate phase input data."""
        pass

    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle phase execution errors."""
        self.logger.error(f"Phase {self.config.name} failed: {error}")
        return {"status": "failed", "error": str(error)}
```

### B. Repository Pattern for Data Access

```python
# src/research_platform/models/repository.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Repository:
    """Domain model for a GitHub repository."""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    language: Optional[str] = None
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    topics: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "description": self.description,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "open_issues": self.open_issues,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "topics": self.topics,
            "metadata": self.metadata
        }

    @classmethod
    def from_github(cls, github_repo) -> 'Repository':
        """Create from PyGithub repository object."""
        return cls(
            id=github_repo.id,
            name=github_repo.name,
            full_name=github_repo.full_name,
            description=github_repo.description,
            language=github_repo.language,
            stars=github_repo.stargazers_count,
            forks=github_repo.forks_count,
            open_issues=github_repo.open_issues_count,
            created_at=github_repo.created_at,
            updated_at=github_repo.updated_at,
            topics=github_repo.get_topics()
        )

# src/research_platform/fetchers/base.py
from abc import ABC, abstractmethod
from typing import List, Optional

class RepositoryFetcher(ABC):
    """Abstract base for repository data fetching."""

    @abstractmethod
    async def fetch_repositories(self, org_name: str) -> List[Repository]:
        """Fetch repositories for an organization."""
        pass

    @abstractmethod
    async def fetch_repository_details(self, repo: Repository) -> Repository:
        """Fetch detailed information for a repository."""
        pass
```

### C. Async Pipeline with Error Recovery

```python
# src/research_platform/core/orchestrator.py
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from contextlib import asynccontextmanager

@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    success: bool
    phases_completed: List[str]
    errors: Dict[str, str]
    data: Dict[str, Any]
    duration: float

class PipelineOrchestrator:
    """Orchestrate pipeline execution with error recovery."""

    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.phases: List[Phase] = []
        self.context: Dict[str, Any] = {}

    def register_phase(self, phase: Phase) -> None:
        """Register a phase in the pipeline."""
        self.phases.append(phase)

    async def execute_pipeline(self) -> PipelineResult:
        """Execute all registered phases."""
        start_time = asyncio.get_event_loop().time()
        phases_completed = []
        errors = {}

        try:
            for phase in self.phases:
                if not phase.config.enabled:
                    self.logger.info(f"Skipping disabled phase: {phase.config.name}")
                    continue

                try:
                    self.logger.info(f"Executing phase: {phase.config.name}")

                    # Execute with timeout
                    result = await asyncio.wait_for(
                        phase.execute(self.context),
                        timeout=phase.config.timeout
                    )

                    # Update context with phase results
                    self.context.update(result)
                    phases_completed.append(phase.config.name)

                except asyncio.TimeoutError:
                    error_msg = f"Phase {phase.config.name} timed out"
                    self.logger.error(error_msg)
                    errors[phase.config.name] = error_msg

                    if phase.config.retry_count > 0:
                        await self._retry_phase(phase, phase.config.retry_count)

                except Exception as e:
                    errors[phase.config.name] = str(e)
                    self.logger.error(f"Phase {phase.config.name} failed: {e}")

        finally:
            duration = asyncio.get_event_loop().time() - start_time

        return PipelineResult(
            success=len(errors) == 0,
            phases_completed=phases_completed,
            errors=errors,
            data=self.context,
            duration=duration
        )

    async def _retry_phase(self, phase: Phase, retries: int) -> Optional[Dict[str, Any]]:
        """Retry a failed phase with exponential backoff."""
        for attempt in range(retries):
            wait_time = 2 ** attempt  # Exponential backoff
            self.logger.info(f"Retrying {phase.config.name} in {wait_time}s...")
            await asyncio.sleep(wait_time)

            try:
                return await phase.execute(self.context)
            except Exception as e:
                if attempt == retries - 1:
                    raise
                self.logger.warning(f"Retry {attempt + 1} failed: {e}")
```

## 3. Testing Infrastructure

### A. Unit Test Example

```python
# tests/unit/test_fetchers/test_github_fetcher.py
import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from research_platform.fetchers.github_fetcher import GitHubFetcher
from research_platform.models.repository import Repository

class TestGitHubFetcher:
    """Test suite for GitHub fetcher."""

    @pytest.fixture
    def mock_github_client(self):
        """Create mock GitHub client."""
        client = Mock()
        return client

    @pytest.fixture
    def fetcher(self, mock_github_client):
        """Create fetcher instance with mock client."""
        fetcher = GitHubFetcher(client=mock_github_client)
        return fetcher

    @pytest.mark.asyncio
    async def test_fetch_repositories_success(self, fetcher, mock_github_client):
        """Test successful repository fetching."""
        # Arrange
        mock_repo = Mock()
        mock_repo.id = 123
        mock_repo.name = "test-repo"
        mock_repo.full_name = "org/test-repo"
        mock_repo.description = "Test repository"
        mock_repo.language = "Python"
        mock_repo.stargazers_count = 10
        mock_repo.forks_count = 5
        mock_repo.open_issues_count = 2
        mock_repo.created_at = datetime.now()
        mock_repo.updated_at = datetime.now()
        mock_repo.get_topics.return_value = ["research", "ml"]

        mock_org = Mock()
        mock_org.get_repos.return_value = [mock_repo]
        mock_github_client.get_organization.return_value = mock_org

        # Act
        repos = await fetcher.fetch_repositories("test-org")

        # Assert
        assert len(repos) == 1
        assert repos[0].name == "test-repo"
        assert repos[0].stars == 10
        assert "research" in repos[0].topics

    @pytest.mark.asyncio
    async def test_fetch_repositories_with_rate_limit(self, fetcher, mock_github_client):
        """Test handling of GitHub rate limits."""
        # Arrange
        mock_github_client.get_organization.side_effect = Exception("API rate limit exceeded")

        # Act & Assert
        with pytest.raises(Exception, match="rate limit"):
            await fetcher.fetch_repositories("test-org")

    @pytest.mark.parametrize("repo_count", [0, 1, 10, 100])
    @pytest.mark.asyncio
    async def test_fetch_multiple_repositories(self, fetcher, mock_github_client, repo_count):
        """Test fetching various numbers of repositories."""
        # Arrange
        mock_repos = []
        for i in range(repo_count):
            mock_repo = Mock()
            mock_repo.id = i
            mock_repo.name = f"repo-{i}"
            mock_repo.full_name = f"org/repo-{i}"
            mock_repos.append(mock_repo)

        mock_org = Mock()
        mock_org.get_repos.return_value = mock_repos
        mock_github_client.get_organization.return_value = mock_org

        # Act
        repos = await fetcher.fetch_repositories("test-org")

        # Assert
        assert len(repos) == repo_count
```

### B. Integration Test Example

```python
# tests/integration/test_pipeline.py
import pytest
import asyncio
from pathlib import Path
import json

from research_platform.core.orchestrator import PipelineOrchestrator
from research_platform.config.settings import Settings

class TestPipelineIntegration:
    """Integration tests for complete pipeline."""

    @pytest.fixture
    def test_config(self, tmp_path):
        """Create test configuration."""
        return {
            "organization": "test-org",
            "output_dir": str(tmp_path / "output"),
            "cache_dir": str(tmp_path / "cache"),
            "phases": {
                "fetch": {"enabled": True, "timeout": 30},
                "analyze": {"enabled": True, "timeout": 60},
                "generate": {"enabled": True, "timeout": 30}
            }
        }

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_full_pipeline_execution(self, test_config):
        """Test complete pipeline execution."""
        # Arrange
        orchestrator = PipelineOrchestrator(test_config, logging.getLogger())

        # Register test phases
        from tests.fixtures.mock_phases import MockFetchPhase, MockAnalyzePhase
        orchestrator.register_phase(MockFetchPhase(test_config))
        orchestrator.register_phase(MockAnalyzePhase(test_config))

        # Act
        result = await orchestrator.execute_pipeline()

        # Assert
        assert result.success
        assert len(result.phases_completed) == 2
        assert "repositories" in result.data
        assert result.duration > 0

    @pytest.mark.asyncio
    async def test_pipeline_with_failure_recovery(self, test_config):
        """Test pipeline recovery from phase failure."""
        # Arrange
        orchestrator = PipelineOrchestrator(test_config, logging.getLogger())

        from tests.fixtures.mock_phases import FailingPhase, RecoverPhase
        orchestrator.register_phase(FailingPhase(test_config))
        orchestrator.register_phase(RecoverPhase(test_config))

        # Act
        result = await orchestrator.execute_pipeline()

        # Assert
        assert not result.success
        assert "FailingPhase" in result.errors
        assert "RecoverPhase" in result.phases_completed
```

## 4. Configuration Management

```python
# src/research_platform/config/settings.py
from typing import Dict, Any, Optional
from pathlib import Path
import os
import yaml
from dataclasses import dataclass, field

@dataclass
class DatabaseConfig:
    """Database configuration."""
    host: str = "localhost"
    port: int = 5432
    name: str = "research_platform"
    user: str = "user"
    password: str = ""

@dataclass
class GitHubConfig:
    """GitHub API configuration."""
    token: str = ""
    organization: str = ""
    rate_limit_pause: int = 60
    max_retries: int = 3

@dataclass
class CacheConfig:
    """Caching configuration."""
    enabled: bool = True
    ttl: int = 3600  # 1 hour
    directory: Path = Path("cache")
    max_size_mb: int = 100

@dataclass
class Settings:
    """Application settings."""
    app_name: str = "GitHub Research Platform"
    debug: bool = False
    log_level: str = "INFO"
    output_directory: Path = Path("output")
    data_directory: Path = Path("data")

    github: GitHubConfig = field(default_factory=GitHubConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    database: Optional[DatabaseConfig] = None

    phases: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, config_path: Path) -> "Settings":
        """Load settings from YAML file."""
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        # Override with environment variables
        config_data = cls._override_with_env(config_data)

        return cls(**config_data)

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            github=GitHubConfig(
                token=os.getenv("GITHUB_TOKEN", ""),
                organization=os.getenv("GITHUB_ORG", "")
            )
        )

    @staticmethod
    def _override_with_env(config: Dict[str, Any]) -> Dict[str, Any]:
        """Override configuration with environment variables."""
        env_mapping = {
            "GITHUB_TOKEN": ("github", "token"),
            "GITHUB_ORG": ("github", "organization"),
            "DEBUG": ("debug",),
            "LOG_LEVEL": ("log_level",),
        }

        for env_var, path in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                current = config
                for key in path[:-1]:
                    current = current.setdefault(key, {})
                current[path[-1]] = value

        return config

# Usage example
settings = Settings.from_yaml(Path("configs/production.yaml"))
```

## 5. Error Handling & Robustness

```python
# src/research_platform/core/exceptions.py
class PlatformException(Exception):
    """Base exception for research platform."""
    pass

class DataFetchException(PlatformException):
    """Exception raised during data fetching."""
    pass

class AnalysisException(PlatformException):
    """Exception raised during analysis."""
    pass

class ValidationException(PlatformException):
    """Exception raised for validation errors."""
    pass

# src/research_platform/utils/validators.py
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of validation."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class DataValidator:
    """Validate data throughout the pipeline."""

    @staticmethod
    def validate_repository_data(data: Dict[str, Any]) -> ValidationResult:
        """Validate repository data structure."""
        errors = []
        warnings = []

        # Required fields
        required = ["id", "name", "full_name"]
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # Data types
        if "stars" in data and not isinstance(data["stars"], int):
            errors.append("Field 'stars' must be an integer")

        # Warnings for missing optional fields
        optional = ["description", "language", "topics"]
        for field in optional:
            if field not in data:
                warnings.append(f"Missing optional field: {field}")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

# src/research_platform/fetchers/github_fetcher.py
class GitHubFetcher(RepositoryFetcher):
    """GitHub API data fetcher with error handling."""

    async def fetch_repositories(self, org_name: str) -> List[Repository]:
        """Fetch repositories with rate limit handling."""
        repos = []

        try:
            async with self._rate_limiter:
                github_repos = await self._fetch_from_api(org_name)

                for github_repo in github_repos:
                    try:
                        repo = Repository.from_github(github_repo)

                        # Validate data
                        validation = DataValidator.validate_repository_data(repo.to_dict())
                        if not validation.valid:
                            self.logger.error(f"Invalid repo data: {validation.errors}")
                            continue

                        if validation.warnings:
                            self.logger.warning(f"Repo warnings: {validation.warnings}")

                        repos.append(repo)

                    except Exception as e:
                        self.logger.error(f"Error processing repo {github_repo.name}: {e}")
                        continue

        except RateLimitExceededException:
            self.logger.warning("Rate limit exceeded, waiting...")
            await asyncio.sleep(self.config.rate_limit_pause)
            return await self.fetch_repositories(org_name)  # Retry

        except Exception as e:
            raise DataFetchException(f"Failed to fetch repositories: {e}")

        return repos
```

## 6. Performance Optimizations

```python
# src/research_platform/fetchers/cache.py
import hashlib
import pickle
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta
import aiofiles
import asyncio

class AsyncCache:
    """Asynchronous cache implementation."""

    def __init__(self, cache_dir: Path, ttl: int = 3600):
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()

    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path from key."""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        async with self._lock:
            try:
                async with aiofiles.open(cache_path, 'rb') as f:
                    data = pickle.loads(await f.read())

                # Check expiration
                if datetime.now() - data['timestamp'] > timedelta(seconds=self.ttl):
                    cache_path.unlink()
                    return None

                return data['value']

            except Exception:
                return None

    async def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        cache_path = self._get_cache_path(key)

        async with self._lock:
            data = {
                'timestamp': datetime.now(),
                'value': value
            }

            async with aiofiles.open(cache_path, 'wb') as f:
                await f.write(pickle.dumps(data))

# src/research_platform/fetchers/parallel_fetcher.py
class ParallelFetcher:
    """Fetch data in parallel with rate limiting."""

    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.cache = AsyncCache(Path("cache"))

    async def fetch_all_repositories(self, org_names: List[str]) -> Dict[str, List[Repository]]:
        """Fetch repositories from multiple organizations in parallel."""
        tasks = []

        for org_name in org_names:
            task = self._fetch_org_with_cache(org_name)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            org: repos
            for org, repos in zip(org_names, results)
            if not isinstance(repos, Exception)
        }

    async def _fetch_org_with_cache(self, org_name: str) -> List[Repository]:
        """Fetch organization data with caching."""
        cache_key = f"org_{org_name}"

        # Try cache first
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        # Fetch with rate limiting
        async with self.semaphore:
            fetcher = GitHubFetcher()
            repos = await fetcher.fetch_repositories(org_name)

            # Cache results
            await self.cache.set(cache_key, repos)

            return repos
```

## 7. Documentation & Maintainability

```python
# src/research_platform/__init__.py
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
https://github.com/your-org/github-research-platform
"""

__version__ = "2.0.0"
__author__ = "Your Organization"

from .core.orchestrator import PipelineOrchestrator
from .config.settings import Settings
from .models.repository import Repository

__all__ = ["PipelineOrchestrator", "Settings", "Repository"]
```

## Implementation Priorities

1. **Phase 1 - Core Refactoring** (Week 1-2)
   - Extract models and data structures
   - Implement dependency injection
   - Create configuration management

2. **Phase 2 - Testing Infrastructure** (Week 2-3)
   - Set up pytest framework
   - Write unit tests for critical paths
   - Add integration tests for pipeline

3. **Phase 3 - Async & Performance** (Week 3-4)
   - Convert to async operations
   - Implement caching layer
   - Add parallel processing

4. **Phase 4 - Error Handling** (Week 4)
   - Add comprehensive error handling
   - Implement retry mechanisms
   - Add validation throughout

5. **Phase 5 - Documentation** (Ongoing)
   - Add docstrings to all public APIs
   - Create user documentation
   - Add architecture diagrams

## Testing Strategy

### Coverage Goals
- Unit tests: 80% coverage minimum
- Integration tests: All critical paths
- Performance tests: Key bottlenecks
- End-to-end tests: Full pipeline

### Test Categories
1. **Unit Tests**
   - All public methods
   - Edge cases and error conditions
   - Data validation

2. **Integration Tests**
   - API interactions
   - Database operations
   - File system operations

3. **Performance Tests**
   - Large dataset handling
   - Concurrent operations
   - Memory usage

4. **End-to-End Tests**
   - Complete pipeline execution
   - Error recovery
   - Output validation

## Monitoring & Observability

```python
# src/research_platform/utils/monitoring.py
import time
from functools import wraps
from typing import Callable
import logging

def monitor_performance(func: Callable) -> Callable:
    """Decorator to monitor function performance."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logger = logging.getLogger(func.__module__)

        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time

            logger.info(f"{func.__name__} completed in {duration:.2f}s")

            # Send metrics to monitoring service
            metrics.record_duration(func.__name__, duration)

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} failed after {duration:.2f}s: {e}")

            # Record error metrics
            metrics.record_error(func.__name__, str(e))

            raise

    return wrapper
```

## Deployment Considerations

1. **Containerization**
   - Create Dockerfile for consistent environments
   - Use multi-stage builds for smaller images
   - Include health checks

2. **CI/CD Pipeline**
   - Run tests on every commit
   - Automate code quality checks
   - Deploy to staging before production

3. **Configuration Management**
   - Use environment-specific configs
   - Secure sensitive data (tokens, keys)
   - Support configuration hot-reloading

4. **Scalability**
   - Design for horizontal scaling
   - Use message queues for long-running tasks
   - Implement distributed caching

This architecture provides a solid foundation for a production-ready, maintainable, and testable research platform.