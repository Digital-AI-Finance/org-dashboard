"""GitHub data fetcher with caching and rate limiting."""

import asyncio
import logging
from typing import Any

from github import Github, GithubException

from ..config.settings import Settings
from ..models.repository import Repository
from .base import BaseFetcher
from .cache import CacheManager


class GitHubFetcher(BaseFetcher):
    """Fetch repository data from GitHub API."""

    def __init__(
        self,
        settings: Settings,
        cache_manager: CacheManager | None = None,
        logger: logging.Logger | None = None,
    ):
        self.settings = settings
        self.cache = cache_manager or CacheManager(settings)
        self.logger = logger or logging.getLogger(__name__)
        self.github = Github(settings.github_token) if settings.github_token else Github()

    async def fetch(self, org_name: str) -> dict[str, Any]:
        """
        Fetch all repository data for an organization.

        Args:
            org_name: GitHub organization name

        Returns:
            Dictionary containing repos and statistics
        """
        # Check cache first
        cache_key = f"org_data_{org_name}"
        cached = await self.cache.get(cache_key)
        if cached:
            self.logger.info(f"Using cached data for {org_name}")
            return cached

        self.logger.info(f"Fetching data for organization: {org_name}")

        try:
            org = self.github.get_organization(org_name)
        except GithubException as e:
            self.logger.error(f"Failed to fetch organization: {e}")
            raise

        # Fetch repositories
        repos = await self._fetch_repositories(org)

        # Calculate statistics
        stats = self._calculate_stats(repos)

        result = {"repos": repos, "stats": stats, "organization": org_name}

        # Cache result
        await self.cache.set(cache_key, result, ttl=self.settings.cache_ttl_seconds)

        return result

    async def _fetch_repositories(self, org: Any) -> list[Repository]:
        """Fetch all repositories for an organization."""
        repositories = []

        for repo in org.get_repos():
            try:
                repo_model = await self._convert_to_model(repo)
                repositories.append(repo_model)
                self.logger.debug(f"Fetched: {repo.name}")
            except Exception as e:
                self.logger.warning(f"Failed to fetch {repo.name}: {e}")
                continue

        return repositories

    async def _convert_to_model(self, repo: Any) -> Repository:
        """
        Convert GitHub repository to domain model.

        Runs in executor to avoid blocking on API calls.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_convert, repo)

    def _sync_convert(self, repo: Any) -> Repository:
        """Synchronous conversion (called in executor)."""
        # Get README
        try:
            readme = repo.get_readme()
            readme_content = readme.decoded_content.decode("utf-8")
        except Exception:
            readme_content = "No README available"

        # Get contributors count
        try:
            contributors_count = repo.get_contributors().totalCount
        except Exception:
            contributors_count = 0

        # Build repository model
        return Repository(
            name=repo.name,
            full_name=repo.full_name,
            description=repo.description or "",
            url=repo.html_url,
            language=repo.language or "Unknown",
            topics=list(repo.get_topics()),
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            watchers=repo.watchers_count,
            open_issues=repo.open_issues_count,
            size=repo.size,
            default_branch=repo.default_branch,
            created_at=repo.created_at.isoformat() if repo.created_at else "",
            updated_at=repo.updated_at.isoformat() if repo.updated_at else "",
            pushed_at=repo.pushed_at.isoformat() if repo.pushed_at else "",
            license=repo.license.name if repo.license else "No License",
            has_wiki=repo.has_wiki,
            has_pages=repo.has_pages,
            archived=repo.archived,
            contributors_count=contributors_count,
            readme=readme_content[:1000],  # Truncate for storage
        )

    def _calculate_stats(self, repos: list[Repository]) -> dict[str, Any]:
        """Calculate organization statistics."""
        return {
            "total_repos": len(repos),
            "active_repos": sum(1 for r in repos if not r.archived),
            "archived_repos": sum(1 for r in repos if r.archived),
            "total_stars": sum(r.stars for r in repos),
            "total_forks": sum(r.forks for r in repos),
            "total_contributors": sum(r.contributors_count for r in repos),
            "avg_stars": sum(r.stars for r in repos) / len(repos) if repos else 0,
            "avg_forks": sum(r.forks for r in repos) / len(repos) if repos else 0,
        }

    async def validate(self, data: dict[str, Any]) -> bool:
        """Validate fetched data."""
        required_keys = ["repos", "stats", "organization"]
        return all(key in data for key in required_keys)
