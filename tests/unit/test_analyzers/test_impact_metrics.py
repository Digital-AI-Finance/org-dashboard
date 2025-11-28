"""Tests for ImpactMetricsAnalyzer."""

import json

import pytest

from research_platform.analyzers.impact_metrics import ImpactMetricsAnalyzer
from research_platform.models.repository import Repository


@pytest.fixture
def impact_analyzer():
    """Create ImpactMetricsAnalyzer instance."""
    return ImpactMetricsAnalyzer()


@pytest.fixture
def repo_with_publications():
    """Create a repository with publications."""
    return Repository(
        id=1,
        name="test-repo",
        full_name="org/test-repo",
        research_metadata={
            "publications": [
                {"title": "Paper 1", "citations": 10, "citation_count": 10},
                {"title": "Paper 2", "citations": 8, "citation_count": 8},
                {"title": "Paper 3", "citations": 5, "citation_count": 5},
                {"title": "Paper 4", "citations": 3, "citation_count": 3},
            ]
        },
    )


@pytest.fixture
def repo_without_publications():
    """Create a repository without publications."""
    return Repository(id=2, name="no-pubs", full_name="org/no-pubs", research_metadata={})


class TestImpactMetricsAnalyzer:
    """Tests for ImpactMetricsAnalyzer functionality."""

    def test_calculate_h_index_empty(self, impact_analyzer):
        """Test h-index calculation with empty list."""
        assert impact_analyzer.calculate_h_index([]) == 0

    def test_calculate_h_index_single_paper(self, impact_analyzer):
        """Test h-index with single paper."""
        assert impact_analyzer.calculate_h_index([5]) == 1
        assert impact_analyzer.calculate_h_index([0]) == 0

    def test_calculate_h_index_multiple_papers(self, impact_analyzer):
        """Test h-index with multiple papers."""
        # Classic h-index examples
        assert impact_analyzer.calculate_h_index([10, 8, 5, 4, 3]) == 4
        assert impact_analyzer.calculate_h_index([25, 8, 5, 3, 3]) == 3
        assert impact_analyzer.calculate_h_index([100, 50, 25, 10, 5, 1]) == 5

    def test_calculate_h_index_all_zeros(self, impact_analyzer):
        """Test h-index with no citations."""
        assert impact_analyzer.calculate_h_index([0, 0, 0, 0]) == 0

    def test_calculate_h_index_unsorted_input(self, impact_analyzer):
        """Test h-index with unsorted citation counts."""
        # Should work regardless of input order
        assert impact_analyzer.calculate_h_index([3, 10, 5, 8, 4]) == 4

    def test_calculate_repository_impact_with_publications(
        self, impact_analyzer, repo_with_publications
    ):
        """Test impact calculation for repo with publications."""
        impact = impact_analyzer.calculate_repository_impact(repo_with_publications)

        assert impact["repository"] == "test-repo"
        assert impact["has_publications"] is True
        assert impact["total_publications"] == 4
        assert impact["total_citations"] == 26  # 10+8+5+3
        assert impact["h_index"] == 3  # 3 papers with ≥3 citations
        assert impact["average_citations"] == 6.5  # 26/4
        assert impact["max_citations"] == 10

    def test_calculate_repository_impact_without_publications(
        self, impact_analyzer, repo_without_publications
    ):
        """Test impact calculation for repo without publications."""
        impact = impact_analyzer.calculate_repository_impact(repo_without_publications)

        assert impact["repository"] == "no-pubs"
        assert impact["has_publications"] is False
        assert impact["total_publications"] == 0
        assert impact["total_citations"] == 0
        assert impact["h_index"] == 0
        assert impact["average_citations"] == 0.0
        assert impact["max_citations"] == 0

    def test_calculate_repository_impact_no_research_metadata(self, impact_analyzer):
        """Test impact calculation for repo with no research metadata."""
        repo = Repository(
            id=3, name="no-metadata", full_name="org/no-metadata", research_metadata=None
        )

        impact = impact_analyzer.calculate_repository_impact(repo)

        assert impact["has_publications"] is False
        assert impact["total_publications"] == 0

    def test_calculate_repository_impact_citation_fallback(self, impact_analyzer):
        """Test that analyzer handles both 'citations' and 'citation_count' fields."""
        repo = Repository(
            id=4,
            name="fallback-test",
            full_name="org/fallback",
            research_metadata={
                "publications": [
                    {"title": "Paper A", "citation_count": 15},  # Only citation_count
                    {"title": "Paper B", "citations": 10},  # Only citations
                    {"title": "Paper C"},  # Missing both (defaults to 0)
                ]
            },
        )

        impact = impact_analyzer.calculate_repository_impact(repo)

        assert impact["total_citations"] == 25  # 15+10+0
        assert impact["total_publications"] == 3

    def test_analyze_organization_impact(
        self, impact_analyzer, repo_with_publications, repo_without_publications
    ):
        """Test organization-wide impact analysis."""
        repos = [repo_with_publications, repo_without_publications]

        result = impact_analyzer.analyze_organization_impact(repos)

        org_metrics = result["organization_metrics"]
        assert org_metrics["total_repositories"] == 2
        assert org_metrics["repositories_with_publications"] == 1
        assert org_metrics["total_publications"] == 4
        assert org_metrics["total_citations"] == 26
        assert org_metrics["organization_h_index"] == 3

    def test_analyze_organization_multiple_repos(self, impact_analyzer):
        """Test organization analysis with multiple repos."""
        repo1 = Repository(
            id=1,
            name="repo1",
            full_name="org/repo1",
            research_metadata={
                "publications": [
                    {"citations": 100},
                    {"citations": 50},
                    {"citations": 25},
                ]
            },
        )
        repo2 = Repository(
            id=2,
            name="repo2",
            full_name="org/repo2",
            research_metadata={"publications": [{"citations": 10}, {"citations": 5}]},
        )

        result = impact_analyzer.analyze_organization_impact([repo1, repo2])

        org_metrics = result["organization_metrics"]
        assert org_metrics["total_publications"] == 5
        assert org_metrics["total_citations"] == 190  # 100+50+25+10+5
        # Org h-index: [100, 50, 25, 10, 5] -> h=5 (all 5 papers with ≥5 citations)
        assert org_metrics["organization_h_index"] == 5

    def test_top_repositories_rankings(self, impact_analyzer):
        """Test that top repositories are correctly ranked."""
        repos = [
            Repository(
                id=1,
                name="high-impact",
                full_name="org/high-impact",
                research_metadata={
                    "publications": [
                        {"citations": 100},
                        {"citations": 80},
                        {"citations": 60},
                    ]
                },
            ),
            Repository(
                id=2,
                name="medium-impact",
                full_name="org/medium",
                research_metadata={"publications": [{"citations": 50}, {"citations": 40}]},
            ),
            Repository(
                id=3,
                name="low-impact",
                full_name="org/low",
                research_metadata={"publications": [{"citations": 10}]},
            ),
        ]

        result = impact_analyzer.analyze_organization_impact(repos)

        # Check top by h-index
        top_h = result["top_repositories_by_h_index"]
        assert len(top_h) == 3
        assert top_h[0]["repository"] == "high-impact"
        assert top_h[0]["h_index"] == 3

        # Check top by citations
        top_cites = result["top_repositories_by_citations"]
        assert len(top_cites) == 3
        assert top_cites[0]["repository"] == "high-impact"
        assert top_cites[0]["total_citations"] == 240

    def test_save_impact_report(self, impact_analyzer, temp_dir):
        """Test saving impact report to JSON file."""
        impact_data = {
            "organization_metrics": {
                "total_publications": 10,
                "total_citations": 100,
                "organization_h_index": 5,
            },
            "repository_impacts": [],
        }

        output_path = temp_dir / "impact_report.json"
        impact_analyzer.save_impact_report(impact_data, output_path)

        assert output_path.exists()

        # Verify content
        with open(output_path, encoding="utf-8") as f:
            loaded_data = json.load(f)

        assert loaded_data["organization_metrics"]["total_publications"] == 10
        assert loaded_data["organization_metrics"]["organization_h_index"] == 5

    def test_median_calculation_odd_count(self, impact_analyzer):
        """Test median calculation with odd number of values."""
        assert impact_analyzer._calculate_median([1, 2, 3, 4, 5]) == 3.0

    def test_median_calculation_even_count(self, impact_analyzer):
        """Test median calculation with even number of values."""
        assert impact_analyzer._calculate_median([1, 2, 3, 4]) == 2.5

    def test_median_calculation_empty(self, impact_analyzer):
        """Test median calculation with empty list."""
        assert impact_analyzer._calculate_median([]) == 0.0

    def test_median_calculation_single(self, impact_analyzer):
        """Test median calculation with single value."""
        assert impact_analyzer._calculate_median([42]) == 42.0

    def test_citation_distribution_in_impact(self, impact_analyzer, repo_with_publications):
        """Test that citation distribution is included in impact metrics."""
        impact = impact_analyzer.calculate_repository_impact(repo_with_publications)

        assert "citation_distribution" in impact
        assert "median" in impact["citation_distribution"]
        assert "top_cited" in impact["citation_distribution"]
        assert impact["citation_distribution"]["median"] == 6.5  # median of [10,8,5,3]
        assert impact["citation_distribution"]["top_cited"] == 10

    def test_average_citations_per_publication_org_level(self, impact_analyzer):
        """Test organization-level average citations calculation."""
        repo = Repository(
            id=1,
            name="test",
            full_name="org/test",
            research_metadata={"publications": [{"citations": 100}, {"citations": 50}]},
        )

        result = impact_analyzer.analyze_organization_impact([repo])

        org_metrics = result["organization_metrics"]
        assert org_metrics["average_citations_per_publication"] == 75.0  # (100+50)/2

    def test_organization_with_no_publications(self, impact_analyzer):
        """Test organization analysis when no repos have publications."""
        repo1 = Repository(id=1, name="repo1", full_name="org/repo1")
        repo2 = Repository(id=2, name="repo2", full_name="org/repo2")

        result = impact_analyzer.analyze_organization_impact([repo1, repo2])

        org_metrics = result["organization_metrics"]
        assert org_metrics["total_publications"] == 0
        assert org_metrics["total_citations"] == 0
        assert org_metrics["organization_h_index"] == 0
        assert org_metrics["average_citations_per_publication"] == 0.0
