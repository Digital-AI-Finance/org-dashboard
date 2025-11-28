"""Research impact metrics calculator.

Calculates academic impact metrics including h-index, total citations,
and other scholarly metrics for repositories with publications.
"""

import json
import logging
from pathlib import Path
from typing import Any

from ..models.repository import Repository


class ImpactMetricsAnalyzer:
    """Calculate research impact metrics from publication data."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)

    def calculate_h_index(self, citation_counts: list[int]) -> int:
        """
        Calculate h-index from a list of citation counts.

        The h-index is the largest number h such that h publications
        have at least h citations each.

        Args:
            citation_counts: List of citation counts for publications

        Returns:
            The h-index value
        """
        if not citation_counts:
            return 0

        # Sort in descending order
        sorted_citations = sorted(citation_counts, reverse=True)

        h_index = 0
        for i, citations in enumerate(sorted_citations, start=1):
            if citations >= i:
                h_index = i
            else:
                break

        return h_index

    def calculate_repository_impact(self, repository: Repository) -> dict[str, Any]:
        """
        Calculate impact metrics for a single repository.

        Args:
            repository: Repository model with research metadata

        Returns:
            Dictionary containing impact metrics
        """
        research_metadata = repository.research_metadata
        publications = research_metadata.get("publications", []) if research_metadata else []

        if not publications:
            return {
                "repository": repository.name,
                "has_publications": False,
                "total_publications": 0,
                "total_citations": 0,
                "h_index": 0,
                "average_citations": 0.0,
                "max_citations": 0,
            }

        # Extract citation counts
        citation_counts = []
        for pub in publications:
            citations = pub.get("citations", 0) or pub.get("citation_count", 0)
            citation_counts.append(citations)

        total_citations = sum(citation_counts)
        h_index = self.calculate_h_index(citation_counts)

        return {
            "repository": repository.name,
            "has_publications": True,
            "total_publications": len(publications),
            "total_citations": total_citations,
            "h_index": h_index,
            "average_citations": total_citations / len(publications) if publications else 0.0,
            "max_citations": max(citation_counts) if citation_counts else 0,
            "citation_distribution": {
                "median": self._calculate_median(citation_counts),
                "top_cited": citation_counts[0] if citation_counts else 0,
            },
        }

    def analyze_organization_impact(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Calculate aggregated impact metrics across all repositories.

        Args:
            repositories: List of repository models

        Returns:
            Dictionary with organization-wide impact metrics
        """
        repo_impacts = []
        total_publications = 0
        total_citations = 0
        all_citation_counts = []

        for repo in repositories:
            impact = self.calculate_repository_impact(repo)
            repo_impacts.append(impact)

            if impact["has_publications"]:
                total_publications += impact["total_publications"]
                total_citations += impact["total_citations"]

                # Collect all citation counts for org-wide h-index
                research_metadata = repo.research_metadata
                if research_metadata:
                    publications = research_metadata.get("publications", [])
                    for pub in publications:
                        citations = pub.get("citations", 0) or pub.get("citation_count", 0)
                        all_citation_counts.append(citations)

        # Calculate organization-wide h-index
        org_h_index = self.calculate_h_index(all_citation_counts)

        return {
            "organization_metrics": {
                "total_repositories": len(repositories),
                "repositories_with_publications": sum(
                    1 for r in repo_impacts if r["has_publications"]
                ),
                "total_publications": total_publications,
                "total_citations": total_citations,
                "organization_h_index": org_h_index,
                "average_citations_per_publication": (
                    total_citations / total_publications if total_publications > 0 else 0.0
                ),
            },
            "repository_impacts": repo_impacts,
            "top_repositories_by_h_index": sorted(
                [r for r in repo_impacts if r["has_publications"]],
                key=lambda x: x["h_index"],
                reverse=True,
            )[:10],
            "top_repositories_by_citations": sorted(
                [r for r in repo_impacts if r["has_publications"]],
                key=lambda x: x["total_citations"],
                reverse=True,
            )[:10],
        }

    def save_impact_report(self, impact_data: dict[str, Any], output_path: Path) -> None:
        """
        Save impact metrics report to JSON file.

        Args:
            impact_data: Impact metrics dictionary
            output_path: Path to save the JSON report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(impact_data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Impact metrics report saved to {output_path}")

    def _calculate_median(self, numbers: list[int | float]) -> float:
        """Calculate median of a list of numbers."""
        if not numbers:
            return 0.0

        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)

        if n % 2 == 0:
            return (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
        else:
            return float(sorted_numbers[n // 2])


def analyze_all_repositories(repos_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Standalone function to analyze impact metrics for all repositories.

    Args:
        repos_data: List of repository dictionaries (from repos.json)

    Returns:
        Impact metrics dictionary
    """
    # Convert to Repository models
    repositories = [Repository.from_dict(repo_data) for repo_data in repos_data]

    analyzer = ImpactMetricsAnalyzer()
    return analyzer.analyze_organization_impact(repositories)


def generate_impact_report(output_path: str | Path = "data/impact_metrics.json") -> None:
    """
    Generate impact metrics report from existing repository data.

    Args:
        output_path: Path to save the report
    """
    # Load repository data
    repos_file = Path("data/repos.json")
    if not repos_file.exists():
        raise FileNotFoundError(f"Repository data not found: {repos_file}")

    with open(repos_file, encoding="utf-8") as f:
        repos_data = json.load(f)

    # Analyze impact
    impact_data = analyze_all_repositories(repos_data)

    # Save report
    analyzer = ImpactMetricsAnalyzer()
    analyzer.save_impact_report(impact_data, Path(output_path))

    print("\nImpact Metrics Summary:")
    print(f"  - Total publications: {impact_data['organization_metrics']['total_publications']}")
    print(f"  - Total citations: {impact_data['organization_metrics']['total_citations']}")
    print(
        f"  - Organization h-index: {impact_data['organization_metrics']['organization_h_index']}"
    )


if __name__ == "__main__":
    generate_impact_report()
