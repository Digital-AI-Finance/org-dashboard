#!/usr/bin/env python3
"""
Citation tracking system: build citation graphs, track impact over time.
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime
from typing import Any


class CitationGraph:
    """Build and analyze citation networks between repositories and papers."""

    def __init__(self):
        self.nodes = {}  # repo_name -> node data
        self.edges = []  # list of (source, target, type) tuples
        self.citation_counts = defaultdict(int)
        self.temporal_data = defaultdict(list)  # Track citations over time

    def add_repository(self, repo_name: str, publications: list[dict]) -> None:
        """Add a repository and its publications to the graph."""
        self.nodes[repo_name] = {
            "type": "repository",
            "publications": publications,
            "cited_by": [],
            "cites": [],
        }

        # Extract cited works
        for pub in publications:
            # Add citations from BibTeX
            if "bibtex" in pub:
                cited_works = self._extract_citations_from_bibtex(pub["bibtex"])
                self.nodes[repo_name]["cites"].extend(cited_works)

    def build_graph(self, repos_data: list[dict]) -> dict[str, Any]:
        """Build citation graph from repository data."""
        print("Building citation graph...")

        # Add all repositories
        for repo in repos_data:
            research_meta = repo.get("research_metadata", {})
            publications = research_meta.get("publications", [])

            if publications:
                self.add_repository(repo["name"], publications)

        # Build edges
        for repo_name, node in self.nodes.items():
            for cited_work in node["cites"]:
                # Find if cited work is in our repository set
                for other_repo, other_node in self.nodes.items():
                    if other_repo == repo_name:
                        continue

                    # Check if any publication matches
                    for pub in other_node["publications"]:
                        if self._publications_match(cited_work, pub):
                            self.edges.append((repo_name, other_repo, "cites"))
                            other_node["cited_by"].append(repo_name)
                            self.citation_counts[other_repo] += 1

        # Calculate metrics
        graph_data = {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "citation_counts": dict(self.citation_counts),
            "network": {
                "nodes": [
                    {
                        "id": name,
                        "type": data["type"],
                        "citations": self.citation_counts.get(name, 0),
                    }
                    for name, data in self.nodes.items()
                ],
                "edges": [
                    {"source": src, "target": tgt, "type": etype} for src, tgt, etype in self.edges
                ],
            },
        }

        return graph_data

    def calculate_impact_metrics(self) -> dict[str, Any]:
        """Calculate research impact metrics."""
        metrics = {}

        for repo_name, node in self.nodes.items():
            total_citations = self.citation_counts.get(repo_name, 0)
            publications_count = len(node["publications"])

            # Get citation counts from publications
            pub_citations = sum(pub.get("citation_count", 0) for pub in node["publications"])

            metrics[repo_name] = {
                "internal_citations": total_citations,  # From other repos in org
                "external_citations": pub_citations,  # From academic databases
                "total_publications": publications_count,
                "h_index": self._calculate_h_index(node["publications"]),
                "citations_per_paper": pub_citations / publications_count
                if publications_count > 0
                else 0,
            }

        return metrics

    def track_citations_over_time(self, repo_name: str, citation_data: dict) -> None:
        """Track citation counts over time for trend analysis."""
        timestamp = datetime.now().isoformat()

        self.temporal_data[repo_name].append(
            {
                "timestamp": timestamp,
                "internal_citations": self.citation_counts.get(repo_name, 0),
                "external_citations": citation_data.get("external_citations", 0),
                "publications": citation_data.get("total_publications", 0),
            }
        )

    def get_citation_network_stats(self) -> dict[str, Any]:
        """Calculate network statistics."""
        if not self.nodes:
            return {}

        # Calculate centrality metrics
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)

        for src, tgt, _ in self.edges:
            out_degree[src] += 1
            in_degree[tgt] += 1

        # Find most influential (cited) repos
        most_cited = sorted(self.citation_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Find most active (citing) repos
        most_citing = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "most_cited_repos": [{"repo": name, "citations": count} for name, count in most_cited],
            "most_citing_repos": [
                {"repo": name, "citations": count} for name, count in most_citing
            ],
            "average_citations_per_repo": sum(self.citation_counts.values()) / len(self.nodes)
            if self.nodes
            else 0,
            "total_citations": sum(self.citation_counts.values()),
        }

    @staticmethod
    def _extract_citations_from_bibtex(bibtex: str) -> list[str]:
        """Extract citation keys from BibTeX entries."""
        # Extract citation keys from @type{KEY, ...}
        pattern = r"@\w+\{([^,]+),"
        matches = re.findall(pattern, bibtex)
        return matches

    @staticmethod
    def _publications_match(cited: str, pub: dict) -> bool:
        """Check if a cited work matches a publication."""
        # Match by DOI
        if "doi" in pub and pub["doi"]:
            if pub["doi"].lower() in cited.lower():
                return True

        # Match by arXiv ID
        if "arxiv_id" in pub and pub["arxiv_id"]:
            if pub["arxiv_id"] in cited:
                return True

        # Match by title (fuzzy)
        if "title" in pub and pub["title"]:
            title_words = set(pub["title"].lower().split())
            cited_words = set(cited.lower().split())
            # If 60% of title words match, consider it a match
            if len(title_words & cited_words) / len(title_words) > 0.6:
                return True

        return False

    @staticmethod
    def _calculate_h_index(publications: list[dict]) -> int:
        """Calculate h-index from publication citation counts."""
        citations = sorted([pub.get("citation_count", 0) for pub in publications], reverse=True)

        h_index = 0
        for i, citation_count in enumerate(citations, 1):
            if citation_count >= i:
                h_index = i
            else:
                break

        return h_index


class CitationHistoryTracker:
    """Track citation history over time."""

    def __init__(self, history_file="data/citation_history.json"):
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self) -> dict:
        """Load citation history from file."""
        if os.path.exists(self.history_file):
            with open(self.history_file) as f:
                return json.load(f)
        return {}

    def save_history(self) -> None:
        """Save citation history to file."""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def record_snapshot(self, repos_data: list[dict]) -> None:
        """Record current citation counts."""
        timestamp = datetime.now().isoformat()

        for repo in repos_data:
            repo_name = repo["name"]
            research_meta = repo.get("research_metadata", {})
            publications = research_meta.get("publications", [])

            if repo_name not in self.history:
                self.history[repo_name] = []

            # Calculate current metrics
            external_citations = sum(pub.get("citation_count", 0) for pub in publications)

            snapshot = {
                "timestamp": timestamp,
                "external_citations": external_citations,
                "publications_count": len(publications),
                "stars": repo.get("stars", 0),
                "forks": repo.get("forks", 0),
            }

            self.history[repo_name].append(snapshot)

        self.save_history()

    def get_growth_trends(self, repo_name: str) -> dict | None:
        """Get citation growth trends for a repository."""
        if repo_name not in self.history or len(self.history[repo_name]) < 2:
            return None

        history = self.history[repo_name]
        first = history[0]
        last = history[-1]

        # Calculate growth
        citation_growth = last["external_citations"] - first["external_citations"]
        pub_growth = last["publications_count"] - first["publications_count"]

        # Calculate average growth rate
        time_span = len(history)
        avg_citation_growth = citation_growth / time_span if time_span > 0 else 0

        return {
            "total_growth": citation_growth,
            "publication_growth": pub_growth,
            "average_monthly_growth": avg_citation_growth,
            "current_citations": last["external_citations"],
            "snapshots": len(history),
        }


def generate_citation_report(repos_data: list[dict]) -> dict[str, Any]:
    """Generate comprehensive citation report."""
    print("Generating citation report...")

    # Build citation graph
    graph = CitationGraph()
    graph_data = graph.build_graph(repos_data)

    # Calculate impact metrics
    impact_metrics = graph.calculate_impact_metrics()

    # Get network stats
    network_stats = graph.get_citation_network_stats()

    # Track history
    tracker = CitationHistoryTracker()
    tracker.record_snapshot(repos_data)

    # Get trends for top repos
    trends = {}
    for repo in repos_data[:10]:  # Top 10 repos
        repo_name = repo["name"]
        trend = tracker.get_growth_trends(repo_name)
        if trend:
            trends[repo_name] = trend

    report = {
        "generated_at": datetime.now().isoformat(),
        "citation_graph": graph_data,
        "impact_metrics": impact_metrics,
        "network_statistics": network_stats,
        "growth_trends": trends,
    }

    # Save report
    os.makedirs("data", exist_ok=True)
    with open("data/citation_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Citation report saved to data/citation_report.json")
    return report


def main():
    """Test citation tracking."""
    print("Citation Tracking System")
    print("=" * 60)

    # Load repos data
    if os.path.exists("data/repos.json"):
        with open("data/repos.json") as f:
            repos_data = json.load(f)

        report = generate_citation_report(repos_data)

        print("\nCitation Graph:")
        print(f"  Nodes: {report['citation_graph']['nodes']}")
        print(f"  Edges: {report['citation_graph']['edges']}")

        print("\nNetwork Statistics:")
        stats = report["network_statistics"]
        if stats.get("most_cited_repos"):
            print("  Most cited repos:")
            for item in stats["most_cited_repos"][:5]:
                print(f"    - {item['repo']}: {item['citations']} citations")

    else:
        print("No repos data found. Run fetch_org_data_research.py first.")


if __name__ == "__main__":
    main()
