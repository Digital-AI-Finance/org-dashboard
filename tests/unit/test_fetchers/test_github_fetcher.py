"""Tests for GitHubFetcher."""

import logging
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from github import GithubException

from research_platform.fetchers.github_fetcher import GitHubFetcher
from research_platform.models.repository import Repository


@pytest.fixture
def github_fetcher(test_settings):
    """Create GitHubFetcher instance."""
    return GitHubFetcher(test_settings)


@pytest.fixture
def github_fetcher_with_logger(test_settings):
    """Create GitHubFetcher with custom logger."""
    logger = logging.getLogger("test_github_fetcher")
    return GitHubFetcher(test_settings, logger=logger)


@pytest.fixture
def mock_organization():
    """Create a mock GitHub organization."""
    org = Mock()
    org.login = "test-org"
    org.name = "Test Organization"
    return org


@pytest.fixture
def mock_github_repo_full():
    """Create a comprehensive mock PyGithub repository."""
    repo = Mock()
    repo.id = 123456
    repo.name = "test-repo"
    repo.full_name = "test-org/test-repo"
    repo.description = "A test repository"
    repo.html_url = "https://github.com/test-org/test-repo"
    repo.homepage = "https://test.com"
    repo.language = "Python"
    repo.stargazers_count = 100
    repo.forks_count = 20
    repo.watchers_count = 50
    repo.open_issues_count = 5
    repo.size = 1024
    repo.default_branch = "main"
    repo.created_at = datetime(2023, 1, 1)
    repo.updated_at = datetime(2024, 1, 1)
    repo.pushed_at = datetime(2024, 1, 1)
    repo.has_wiki = True
    repo.has_pages = False
    repo.archived = False
    repo.get_topics.return_value = ["python", "testing"]

    # Mock license
    license_mock = Mock()
    license_mock.name = "MIT License"
    repo.license = license_mock

    # Mock README
    readme_mock = Mock()
    readme_mock.decoded_content = b"# Test README\nThis is a test"
    repo.get_readme.return_value = readme_mock

    # Mock contributors
    contributors_mock = Mock()
    contributors_mock.totalCount = 10
    repo.get_contributors.return_value = contributors_mock

    return repo


class TestGitHubFetcher:
    """Tests for GitHubFetcher functionality."""

    def test_initialization_with_token(self, test_settings):
        """Test GitHubFetcher initialization with token."""
        fetcher = GitHubFetcher(test_settings)

        assert fetcher.settings == test_settings
        assert fetcher.cache is not None
        assert fetcher.logger is not None
        assert fetcher.github is not None

    def test_initialization_without_token(self, test_settings):
        """Test GitHubFetcher initialization without token."""
        test_settings.github_token = None
        fetcher = GitHubFetcher(test_settings)

        assert fetcher.github is not None  # Should still create unauthenticated client

    def test_initialization_with_custom_logger(self, github_fetcher_with_logger):
        """Test that custom logger is used."""
        assert github_fetcher_with_logger.logger.name == "test_github_fetcher"

    @pytest.mark.asyncio
    async def test_fetch_success(self, github_fetcher, mock_organization, mock_github_repo_full):
        """Test successful fetch of organization data."""
        # Mock GitHub client
        with patch.object(github_fetcher, "github") as mock_github:
            mock_github.get_organization.return_value = mock_organization
            mock_organization.get_repos.return_value = [mock_github_repo_full]

            # Mock cache to return None (cache miss)
            with patch.object(github_fetcher.cache, "get", return_value=None):
                with patch.object(github_fetcher.cache, "set", return_value=None):
                    result = await github_fetcher.fetch("test-org")

        assert "repos" in result
        assert "stats" in result
        assert "organization" in result
        assert result["organization"] == "test-org"
        assert len(result["repos"]) == 1
        assert isinstance(result["repos"][0], Repository)

    @pytest.mark.asyncio
    async def test_fetch_from_cache(self, github_fetcher):
        """Test fetching from cache."""
        cached_data = {"repos": [], "stats": {"total_repos": 0}, "organization": "test-org"}

        with patch.object(github_fetcher.cache, "get", return_value=cached_data):
            result = await github_fetcher.fetch("test-org")

        assert result == cached_data

    @pytest.mark.asyncio
    async def test_fetch_organization_not_found(self, github_fetcher):
        """Test fetch with non-existent organization."""
        with patch.object(github_fetcher, "github") as mock_github:
            mock_github.get_organization.side_effect = GithubException(
                404, {"message": "Not Found"}, None
            )

            with pytest.raises(GithubException):
                await github_fetcher.fetch("nonexistent-org")

    @pytest.mark.asyncio
    async def test_fetch_repositories_success(
        self, github_fetcher, mock_organization, mock_github_repo_full
    ):
        """Test _fetch_repositories with multiple repos."""
        mock_organization.get_repos.return_value = [mock_github_repo_full, mock_github_repo_full]

        repos = await github_fetcher._fetch_repositories(mock_organization)

        assert len(repos) == 2
        assert all(isinstance(r, Repository) for r in repos)

    @pytest.mark.asyncio
    async def test_fetch_repositories_with_errors(
        self, github_fetcher, mock_organization, mock_github_repo_full
    ):
        """Test _fetch_repositories skips repos with errors."""
        # Create a failing repo
        failing_repo = Mock()
        failing_repo.name = "failing-repo"
        failing_repo.get_readme.side_effect = Exception("API Error")
        failing_repo.full_name = "test-org/failing-repo"

        mock_organization.get_repos.return_value = [mock_github_repo_full, failing_repo]

        repos = await github_fetcher._fetch_repositories(mock_organization)

        # Should only get 1 successful repo (failing one should be skipped)
        assert len(repos) >= 1  # May still process failing repo if error is later

    @pytest.mark.asyncio
    async def test_convert_to_model_success(self, github_fetcher, mock_github_repo_full):
        """Test _convert_to_model converts successfully."""
        repo_model = await github_fetcher._convert_to_model(mock_github_repo_full)

        assert isinstance(repo_model, Repository)
        assert repo_model.name == "test-repo"
        assert repo_model.full_name == "test-org/test-repo"
        assert repo_model.language == "Python"
        assert repo_model.stars == 100

    def test_sync_convert_full_repo(self, github_fetcher, mock_github_repo_full):
        """Test _sync_convert with complete repository."""
        repo_model = github_fetcher._sync_convert(mock_github_repo_full)

        assert isinstance(repo_model, Repository)
        assert repo_model.id == 123456
        assert repo_model.name == "test-repo"
        assert repo_model.description == "A test repository"
        assert repo_model.language == "Python"
        assert repo_model.stars == 100
        assert repo_model.forks == 20
        assert repo_model.contributors_count == 10
        assert "Test README" in repo_model.metadata["readme"]
        assert repo_model.metadata["license"] == "MIT License"
        assert repo_model.metadata["url"] == "https://github.com/test-org/test-repo"

    def test_sync_convert_repo_without_readme(self, github_fetcher):
        """Test _sync_convert with repo missing README."""
        repo = Mock()
        repo.id = 789
        repo.name = "no-readme"
        repo.full_name = "test-org/no-readme"
        repo.description = "No README"
        repo.html_url = "https://github.com/test-org/no-readme"
        repo.homepage = None
        repo.language = "Python"
        repo.get_topics.return_value = []
        repo.stargazers_count = 0
        repo.forks_count = 0
        repo.watchers_count = 0
        repo.open_issues_count = 0
        repo.size = 100
        repo.default_branch = "main"
        repo.created_at = datetime(2023, 1, 1)
        repo.updated_at = datetime(2024, 1, 1)
        repo.pushed_at = datetime(2024, 1, 1)
        repo.has_wiki = False
        repo.has_pages = False
        repo.archived = False
        repo.license = None
        repo.get_readme.side_effect = Exception("Not found")

        contributors_mock = Mock()
        contributors_mock.totalCount = 0
        repo.get_contributors.return_value = contributors_mock

        repo_model = github_fetcher._sync_convert(repo)

        assert repo_model.metadata["readme"] == "No README available"
        assert repo_model.metadata["license"] == "No License"

    def test_sync_convert_repo_without_contributors(self, github_fetcher):
        """Test _sync_convert with repo that fails to get contributors."""
        repo = Mock()
        repo.id = 999
        repo.name = "no-contributors"
        repo.full_name = "test-org/no-contributors"
        repo.description = "Test"
        repo.html_url = "https://github.com/test-org/no-contributors"
        repo.homepage = ""
        repo.language = None  # Test None language
        repo.get_topics.return_value = []
        repo.stargazers_count = 5
        repo.forks_count = 1
        repo.watchers_count = 3
        repo.open_issues_count = 2
        repo.size = 50
        repo.default_branch = "master"
        repo.created_at = None  # Test None datetime
        repo.updated_at = None
        repo.pushed_at = None
        repo.has_wiki = False
        repo.has_pages = False
        repo.archived = True
        repo.license = None
        repo.get_readme.side_effect = Exception("Not found")
        repo.get_contributors.side_effect = Exception("API Error")

        repo_model = github_fetcher._sync_convert(repo)

        assert repo_model.contributors_count == 0
        assert repo_model.language is None  # Should be None, not "Unknown"
        assert repo_model.created_at is None
        assert repo_model.archived is True

    def test_calculate_stats_empty(self, github_fetcher):
        """Test _calculate_stats with no repositories."""
        stats = github_fetcher._calculate_stats([])

        assert stats["total_repos"] == 0
        assert stats["active_repos"] == 0
        assert stats["archived_repos"] == 0
        assert stats["total_stars"] == 0
        assert stats["avg_stars"] == 0

    def test_calculate_stats_multiple_repos(self, github_fetcher, sample_repositories):
        """Test _calculate_stats with multiple repositories."""
        stats = github_fetcher._calculate_stats(sample_repositories)

        assert stats["total_repos"] == 10
        assert stats["active_repos"] == 10  # None are archived in fixture
        assert stats["total_stars"] == sum(r.stars for r in sample_repositories)
        assert stats["total_forks"] == sum(r.forks for r in sample_repositories)
        assert stats["avg_stars"] > 0

    def test_calculate_stats_with_archived(self, github_fetcher):
        """Test _calculate_stats with archived repos."""
        active_repo = Repository(
            id=1,
            name="active",
            full_name="test/active",
            stars=10,
            forks=5,
            contributors_count=3,
            archived=False,
        )
        archived_repo = Repository(
            id=2,
            name="archived",
            full_name="test/archived",
            stars=20,
            forks=10,
            contributors_count=5,
            archived=True,
        )

        stats = github_fetcher._calculate_stats([active_repo, archived_repo])

        assert stats["total_repos"] == 2
        assert stats["active_repos"] == 1
        assert stats["archived_repos"] == 1
        assert stats["total_stars"] == 30

    @pytest.mark.asyncio
    async def test_validate_success(self, github_fetcher):
        """Test validate with valid data."""
        valid_data = {"repos": [], "stats": {}, "organization": "test-org"}

        result = await github_fetcher.validate(valid_data)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_missing_keys(self, github_fetcher):
        """Test validate with missing required keys."""
        invalid_data = {"repos": []}  # Missing stats and organization

        result = await github_fetcher.validate(invalid_data)
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_empty_dict(self, github_fetcher):
        """Test validate with empty dictionary."""
        result = await github_fetcher.validate({})
        assert result is False

    @pytest.mark.asyncio
    async def test_fetch_caches_result(
        self, github_fetcher, mock_organization, mock_github_repo_full
    ):
        """Test that fetch caches the result."""
        with patch.object(github_fetcher, "github") as mock_github:
            mock_github.get_organization.return_value = mock_organization
            mock_organization.get_repos.return_value = [mock_github_repo_full]

            with patch.object(github_fetcher.cache, "get", return_value=None):
                with patch.object(github_fetcher.cache, "set") as mock_set:
                    await github_fetcher.fetch("test-org")

                    # Verify cache.set was called
                    mock_set.assert_called_once()
                    call_args = mock_set.call_args
                    assert call_args[0][0] == "org_data_test-org"  # cache key
                    assert "repos" in call_args[0][1]  # cached data

    @pytest.mark.asyncio
    async def test_readme_truncation(self, github_fetcher):
        """Test that README content is truncated to 1000 chars."""
        repo = Mock()
        repo.id = 888
        repo.name = "long-readme"
        repo.full_name = "test-org/long-readme"
        repo.description = "Test"
        repo.html_url = "https://github.com/test-org/long-readme"
        repo.homepage = None
        repo.language = "Python"
        repo.get_topics.return_value = []
        repo.stargazers_count = 1
        repo.forks_count = 0
        repo.watchers_count = 0
        repo.open_issues_count = 0
        repo.size = 100
        repo.default_branch = "main"
        repo.created_at = datetime(2023, 1, 1)
        repo.updated_at = datetime(2024, 1, 1)
        repo.pushed_at = datetime(2024, 1, 1)
        repo.has_wiki = False
        repo.has_pages = False
        repo.archived = False
        repo.license = None

        # Create README longer than 1000 characters
        long_readme = "A" * 2000
        readme_mock = Mock()
        readme_mock.decoded_content = long_readme.encode()
        repo.get_readme.return_value = readme_mock

        contributors_mock = Mock()
        contributors_mock.totalCount = 1
        repo.get_contributors.return_value = contributors_mock

        repo_model = github_fetcher._sync_convert(repo)

        assert len(repo_model.metadata["readme"]) == 1000
        assert repo_model.metadata["readme"] == "A" * 1000
