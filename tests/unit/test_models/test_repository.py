"""Unit tests for the Repository model."""

from datetime import datetime, timedelta

import pytest

from research_platform.models.repository import Repository


class TestRepository:
    """Test suite for Repository model."""

    def test_repository_creation(self):
        """Test creating a repository instance."""
        repo = Repository(
            id=123,
            name="test-repo",
            full_name="org/test-repo",
            description="Test repository",
            language="Python",
            stars=10,
            forks=5,
        )

        assert repo.id == 123
        assert repo.name == "test-repo"
        assert repo.full_name == "org/test-repo"
        assert repo.description == "Test repository"
        assert repo.language == "Python"
        assert repo.stars == 10
        assert repo.forks == 5

    def test_repository_defaults(self):
        """Test repository default values."""
        repo = Repository(id=123, name="test", full_name="org/test")

        assert repo.stars == 0
        assert repo.forks == 0
        assert repo.open_issues == 0
        assert repo.archived is False
        assert repo.topics == []
        assert repo.metadata == {}

    def test_to_dict(self, sample_repository):
        """Test converting repository to dictionary."""
        data = sample_repository.to_dict()

        assert data["id"] == 123456
        assert data["name"] == "test-repo"
        assert data["full_name"] == "test-org/test-repo"
        assert data["stars"] == 42
        assert "2023-01-01" in data["created_at"]

    def test_from_dict(self):
        """Test creating repository from dictionary."""
        data = {
            "id": 999,
            "name": "from-dict",
            "full_name": "org/from-dict",
            "stars": 100,
            "created_at": "2023-06-01T00:00:00",
        }

        repo = Repository.from_dict(data)

        assert repo.id == 999
        assert repo.name == "from-dict"
        assert repo.stars == 100
        assert isinstance(repo.created_at, datetime)

    def test_from_github(self, mock_github_repo):
        """Test creating repository from GitHub API object."""
        repo = Repository.from_github(mock_github_repo)

        assert repo.id == 123456
        assert repo.name == "test-repo"
        assert repo.full_name == "test-org/test-repo"
        assert repo.stars == 100
        assert repo.forks == 20
        assert repo.contributors_count == 10
        assert "python" in repo.topics

    def test_is_active(self):
        """Test repository active status."""
        # Active repository
        active_repo = Repository(id=1, name="active", full_name="org/active")
        assert active_repo.is_active is True

        # Archived repository
        archived_repo = Repository(id=2, name="archived", full_name="org/archived", archived=True)
        assert archived_repo.is_active is False

        # Disabled repository
        disabled_repo = Repository(id=3, name="disabled", full_name="org/disabled", disabled=True)
        assert disabled_repo.is_active is False

    def test_age_days(self):
        """Test repository age calculation."""
        # Repository created 30 days ago
        repo = Repository(
            id=1, name="test", full_name="org/test", created_at=datetime.now() - timedelta(days=30)
        )

        assert 29 <= repo.age_days <= 31  # Allow for small time differences

        # Repository without created_at
        repo_no_date = Repository(id=2, name="test2", full_name="org/test2")
        assert repo_no_date.age_days == 0

    def test_days_since_update(self):
        """Test days since update calculation."""
        # Repository updated 7 days ago
        repo = Repository(
            id=1, name="test", full_name="org/test", updated_at=datetime.now() - timedelta(days=7)
        )

        assert 6 <= repo.days_since_update <= 8

    def test_add_research_metadata(self, sample_repository):
        """Test adding research metadata."""
        metadata = {
            "paper_url": "https://arxiv.org/paper",
            "dataset_size": "1GB",
            "methodology": "deep learning",
        }

        sample_repository.add_research_metadata(metadata)

        assert sample_repository.research_metadata["paper_url"] == "https://arxiv.org/paper"
        assert sample_repository.research_metadata["dataset_size"] == "1GB"

    def test_add_citation(self, sample_repository):
        """Test adding citations."""
        citation = {
            "title": "Research Paper",
            "authors": ["Author 1", "Author 2"],
            "year": 2024,
            "venue": "Conference",
        }

        sample_repository.add_citation(citation)

        assert len(sample_repository.citations) == 1
        assert sample_repository.citations[0]["title"] == "Research Paper"

    def test_health_score(self):
        """Test repository health score calculation."""
        # High health score repository
        healthy_repo = Repository(
            id=1,
            name="healthy",
            full_name="org/healthy",
            description="Well documented repository",
            homepage="https://docs.example.com",
            stars=100,
            forks=20,
            open_issues=2,
            contributors_count=15,
            updated_at=datetime.now() - timedelta(days=5),
        )

        score = healthy_repo.get_health_score()
        assert 0.5 <= score <= 1.0

        # Low health score repository
        unhealthy_repo = Repository(
            id=2,
            name="unhealthy",
            full_name="org/unhealthy",
            stars=0,
            forks=0,
            open_issues=50,
            contributors_count=1,
            updated_at=datetime.now() - timedelta(days=365),
        )

        score = unhealthy_repo.get_health_score()
        assert 0.0 <= score <= 0.3

    @pytest.mark.parametrize(
        "stars,expected_range",
        [
            (0, (0.0, 0.2)),
            (10, (0.1, 0.4)),
            (100, (0.3, 0.6)),
            (1000, (0.4, 0.8)),
            (10000, (0.5, 1.0)),
        ],
    )
    def test_health_score_stars_impact(self, stars, expected_range):
        """Test how star count affects health score."""
        repo = Repository(id=1, name="test", full_name="org/test", stars=stars)

        score = repo.get_health_score()
        assert expected_range[0] <= score <= expected_range[1]

    def test_string_representation(self, sample_repository):
        """Test string representations."""
        str_repr = str(sample_repository)
        assert "test-org/test-repo" in str_repr
        assert "stars=42" in str_repr

        repr_repr = repr(sample_repository)
        assert "id=123456" in repr_repr
        assert "name='test-repo'" in repr_repr

    def test_repository_equality(self):
        """Test repository equality comparison."""
        repo1 = Repository(id=1, name="test", full_name="org/test")
        repo2 = Repository(id=1, name="test", full_name="org/test")
        repo3 = Repository(id=2, name="other", full_name="org/other")

        assert repo1.id == repo2.id
        assert repo1.id != repo3.id

    def test_repository_with_null_values(self):
        """Test repository with null/None values."""
        repo = Repository(
            id=123,
            name="test",
            full_name="org/test",
            description=None,
            language=None,
            created_at=None,
        )

        data = repo.to_dict()
        assert data["description"] is None
        assert data["language"] is None
        assert data["created_at"] is None

        # Should not raise errors
        assert repo.age_days == 0
        assert repo.days_since_update == 0
