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

        # Get valid field names from the dataclass
        import dataclasses

        valid_fields = {f.name for f in dataclasses.fields(cls)}

        # Filter data to only include valid fields
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        # Generate ID from full_name hash if missing (for backward compatibility)
        if "id" not in filtered_data and "full_name" in filtered_data:
            filtered_data["id"] = abs(hash(filtered_data["full_name"])) % (10**9)

        # Store extra fields in metadata if they exist
        extra_fields = {k: v for k, v in data.items() if k not in valid_fields}
        if extra_fields and "metadata" not in filtered_data:
            filtered_data["metadata"] = {}
        if extra_fields:
            filtered_data["metadata"].update(extra_fields)

        return cls(**filtered_data)

    @classmethod
    def from_github(cls, github_repo) -> "Repository":
        """Create from PyGithub repository object."""
        try:
            topics = list(github_repo.get_topics())
        except Exception:
            topics = []

        try:
            contributors_count = github_repo.get_contributors().totalCount
        except Exception:
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
            # Handle both timezone-aware and naive datetimes
            created = (
                self.created_at.replace(tzinfo=None) if self.created_at.tzinfo else self.created_at
            )
            return (datetime.now() - created).days
        return 0

    @property
    def days_since_update(self) -> int:
        """Get days since last update."""
        if self.updated_at:
            # Handle both timezone-aware and naive datetimes
            updated = (
                self.updated_at.replace(tzinfo=None) if self.updated_at.tzinfo else self.updated_at
            )
            return (datetime.now() - updated).days
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

    def calculate_health_score(self) -> dict[str, Any]:
        """
        Calculate detailed health scores for the repository.

        Returns a dictionary with overall score and breakdown by category.
        """
        import math

        scores = {
            "activity": 0.0,
            "community": 0.0,
            "documentation": 0.0,
            "code_quality": 0.0,
        }

        # Activity score (based on recency and frequency)
        if self.days_since_update < 30:
            scores["activity"] = 25.0
        elif self.days_since_update < 90:
            scores["activity"] = 20.0
        elif self.days_since_update < 180:
            scores["activity"] = 15.0
        elif self.days_since_update < 365:
            scores["activity"] = 10.0
        else:
            scores["activity"] = 5.0

        # Community score (based on stars, forks, contributors)
        community_score = 0.0
        if self.stars > 0:
            community_score += min(math.log10(self.stars + 1) * 5, 10)
        if self.forks > 0:
            community_score += min(math.log10(self.forks + 1) * 3, 7)
        if self.contributors_count > 0:
            community_score += min(self.contributors_count, 8)
        scores["community"] = min(community_score, 25.0)

        # Documentation score
        doc_score = 0.0
        if self.description and len(self.description) > 20:
            doc_score += 10.0
        if self.homepage:
            doc_score += 5.0
        if self.has_wiki:
            doc_score += 5.0
        if len(self.topics) > 0:
            doc_score += min(len(self.topics) * 1.5, 5.0)
        scores["documentation"] = min(doc_score, 25.0)

        # Code quality score (proxy based on available metrics)
        quality_score = 0.0
        if self.has_issues:
            quality_score += 5.0
        if not self.archived:
            quality_score += 5.0
        if not self.disabled:
            quality_score += 5.0
        # Lower open issues ratio is better
        if self.stars > 0:
            issues_ratio = self.open_issues / (self.stars + 1)
            quality_score += max(0, 10 - issues_ratio * 20)
        scores["code_quality"] = min(quality_score, 25.0)

        overall = sum(scores.values())

        return {
            "overall": overall,
            "scores": scores,
            "max_score": 100.0,
            "grade": self._score_to_grade(overall),
        }

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def __str__(self) -> str:
        """String representation."""
        return f"Repository({self.full_name}, stars={self.stars}, language={self.language})"

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Repository(id={self.id}, name='{self.name}', full_name='{self.full_name}')"
