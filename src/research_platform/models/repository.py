"""Repository domain model."""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Repository:
    """Domain model for a GitHub repository."""

    # Required fields
    id: int
    name: str
    full_name: str

    # Basic info
    description: str | None = None
    language: str | None = None
    homepage: str | None = None
    default_branch: str = "main"

    # Statistics
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    open_issues: int = 0
    size: int = 0

    # Timestamps
    created_at: datetime | None = None
    updated_at: datetime | None = None
    pushed_at: datetime | None = None

    # Features
    has_issues: bool = True
    has_projects: bool = True
    has_wiki: bool = True
    has_pages: bool = False
    has_downloads: bool = True
    archived: bool = False
    disabled: bool = False
    is_template: bool = False

    # Lists
    topics: list[str] = field(default_factory=list)

    # Research-specific metadata
    research_metadata: dict[str, Any] = field(default_factory=dict)
    citations: list[dict[str, Any]] = field(default_factory=list)
    contributors_count: int = 0
    commits_count: int = 0

    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        data = asdict(self)

        # Convert datetime objects to ISO format strings
        for field_name in ["created_at", "updated_at", "pushed_at"]:
            if field_name in data and data[field_name]:
                data[field_name] = data[field_name].isoformat()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Repository":
        """Create instance from dictionary."""
        # Convert ISO strings back to datetime objects
        for field_name in ["created_at", "updated_at", "pushed_at"]:
            if field_name in data and data[field_name]:
                if isinstance(data[field_name], str):
                    data[field_name] = datetime.fromisoformat(
                        data[field_name].replace("Z", "+00:00")
                    )

        return cls(**data)

    @classmethod
    def from_github(cls, github_repo) -> "Repository":
        """Create from PyGithub repository object."""
        try:
            topics = list(github_repo.get_topics())
        except:
            topics = []

        try:
            contributors_count = github_repo.get_contributors().totalCount
        except:
            contributors_count = 0

        return cls(
            id=github_repo.id,
            name=github_repo.name,
            full_name=github_repo.full_name,
            description=github_repo.description,
            language=github_repo.language,
            homepage=github_repo.homepage,
            default_branch=github_repo.default_branch,
            stars=github_repo.stargazers_count,
            forks=github_repo.forks_count,
            watchers=github_repo.watchers_count,
            open_issues=github_repo.open_issues_count,
            size=github_repo.size,
            created_at=github_repo.created_at,
            updated_at=github_repo.updated_at,
            pushed_at=github_repo.pushed_at,
            has_issues=github_repo.has_issues,
            has_projects=github_repo.has_projects,
            has_wiki=github_repo.has_wiki,
            has_pages=github_repo.has_pages,
            has_downloads=github_repo.has_downloads,
            archived=github_repo.archived,
            disabled=github_repo.disabled if hasattr(github_repo, "disabled") else False,
            is_template=github_repo.is_template if hasattr(github_repo, "is_template") else False,
            topics=topics,
            contributors_count=contributors_count,
        )

    @property
    def is_active(self) -> bool:
        """Check if repository is active (not archived or disabled)."""
        return not self.archived and not self.disabled

    @property
    def age_days(self) -> int:
        """Get repository age in days."""
        if self.created_at:
            return (datetime.now() - self.created_at).days
        return 0

    @property
    def days_since_update(self) -> int:
        """Get days since last update."""
        if self.updated_at:
            return (datetime.now() - self.updated_at).days
        return 0

    def add_research_metadata(self, metadata: dict[str, Any]) -> None:
        """Add research-specific metadata."""
        self.research_metadata.update(metadata)

    def add_citation(self, citation: dict[str, Any]) -> None:
        """Add a citation reference."""
        self.citations.append(citation)

    def get_health_score(self) -> float:
        """
        Calculate a simple health score based on various metrics.

        Returns value between 0.0 and 1.0
        """
        score = 0.0
        weights = {
            "stars": 0.2,
            "forks": 0.15,
            "contributors": 0.2,
            "recent_update": 0.2,
            "documentation": 0.15,
            "issues_ratio": 0.1,
        }

        # Stars score (logarithmic)
        if self.stars > 0:
            import math

            score += weights["stars"] * min(math.log10(self.stars + 1) / 4, 1.0)

        # Forks score (logarithmic)
        if self.forks > 0:
            import math

            score += weights["forks"] * min(math.log10(self.forks + 1) / 3, 1.0)

        # Contributors score
        if self.contributors_count > 0:
            score += weights["contributors"] * min(self.contributors_count / 20, 1.0)

        # Recent update score
        if self.days_since_update < 90:
            score += weights["recent_update"] * (1 - self.days_since_update / 365)

        # Documentation score
        if self.description:
            score += weights["documentation"] * 0.5
        if self.homepage:
            score += weights["documentation"] * 0.5

        # Issues ratio (fewer open issues is better)
        if self.stars > 0:
            issues_ratio = self.open_issues / (self.stars + 1)
            score += weights["issues_ratio"] * max(0, 1 - issues_ratio)

        return min(score, 1.0)

    def __str__(self) -> str:
        """String representation."""
        return f"Repository({self.full_name}, stars={self.stars}, language={self.language})"

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Repository(id={self.id}, name='{self.name}', full_name='{self.full_name}')"
