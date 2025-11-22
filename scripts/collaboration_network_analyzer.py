#!/usr/bin/env python3
"""
Collaboration network analysis from real git commit history.
Fetches commit data from GitHub API and builds author co-authorship networks.
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Any

try:
    from github import Github, GithubException

    PYGITHUB_AVAILABLE = True
except ImportError:
    print("PyGithub not installed. Install with: pip install PyGithub")
    PYGITHUB_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class CollaborationNetworkAnalyzer:
    """Analyze collaboration networks from git commit history."""

    def __init__(self, github_token: str):
        if not PYGITHUB_AVAILABLE:
            raise ImportError("PyGithub is required")
        self.github = Github(github_token)

    def fetch_commit_authors(self, repo_full_name: str, max_commits=200) -> list[dict[str, Any]]:
        """Fetch commit authors from a repository."""
        try:
            repo = self.github.get_repo(repo_full_name)
            commits = repo.get_commits()

            authors = []
            count = 0

            for commit in commits:
                if count >= max_commits:
                    break

                try:
                    if commit.author:
                        author_info = {
                            "login": commit.author.login if commit.author else None,
                            "name": commit.commit.author.name,
                            "email": commit.commit.author.email,
                            "date": commit.commit.author.date.isoformat(),
                            "sha": commit.sha,
                        }
                        authors.append(author_info)
                        count += 1
                except Exception:
                    # Skip commits with missing author info
                    continue

            return authors

        except GithubException as e:
            print(f"Error fetching commits for {repo_full_name}: {e}")
            return []

    def build_collaboration_network(
        self, repos_data: list[dict[str, Any]], org_name: str
    ) -> dict[str, Any]:
        """Build collaboration network from commit histories."""
        print("Building collaboration network from commit histories...")

        # Repository -> Authors mapping
        repo_authors = defaultdict(set)

        # Author statistics
        author_stats = defaultdict(
            lambda: {
                "repos": set(),
                "commits": 0,
                "first_commit": None,
                "last_commit": None,
                "emails": set(),
            }
        )

        # Fetch commits for each repository
        for repo in repos_data:
            repo_name = repo["name"]
            full_name = f"{org_name}/{repo_name}"

            print(f"  Fetching commits from {repo_name}...")

            authors = self.fetch_commit_authors(full_name, max_commits=200)

            for author in authors:
                # Normalize author identity
                author_login = author.get("login") or author.get("name")
                if not author_login:
                    continue

                # Track repository
                repo_authors[repo_name].add(author_login)

                # Update author stats
                author_stats[author_login]["repos"].add(repo_name)
                author_stats[author_login]["commits"] += 1
                author_stats[author_login]["emails"].add(author.get("email", ""))

                commit_date = datetime.fromisoformat(author["date"].replace("Z", "+00:00"))

                if (
                    author_stats[author_login]["first_commit"] is None
                    or commit_date < author_stats[author_login]["first_commit"]
                ):
                    author_stats[author_login]["first_commit"] = commit_date

                if (
                    author_stats[author_login]["last_commit"] is None
                    or commit_date > author_stats[author_login]["last_commit"]
                ):
                    author_stats[author_login]["last_commit"] = commit_date

        # Build co-authorship edges (authors who worked on same repos)
        edges = defaultdict(int)

        for repo_name, authors in repo_authors.items():
            author_list = list(authors)
            # Create edges between all pairs of authors in this repo
            for i, author1 in enumerate(author_list):
                for author2 in author_list[i + 1 :]:
                    # Create sorted tuple for undirected edge
                    edge = tuple(sorted([author1, author2]))
                    edges[edge] += 1  # Weight by number of shared repos

        # Convert to network format
        nodes = []
        for author, stats in author_stats.items():
            nodes.append(
                {
                    "id": author,
                    "repos": list(stats["repos"]),
                    "repo_count": len(stats["repos"]),
                    "commit_count": stats["commits"],
                    "first_commit": stats["first_commit"].isoformat()
                    if stats["first_commit"]
                    else None,
                    "last_commit": stats["last_commit"].isoformat()
                    if stats["last_commit"]
                    else None,
                    "emails": list(stats["emails"]),
                }
            )

        edge_list = []
        for (source, target), weight in edges.items():
            edge_list.append(
                {"source": source, "target": target, "weight": weight, "shared_repos": weight}
            )

        network = {"nodes": nodes, "edges": edge_list}

        # Calculate network metrics
        metrics = self.calculate_network_metrics(network)

        return {
            "generated_at": datetime.now().isoformat(),
            "organization": org_name,
            "network": network,
            "metrics": metrics,
            "summary": {
                "total_authors": len(nodes),
                "total_collaborations": len(edge_list),
                "total_commits": sum(n["commit_count"] for n in nodes),
                "repositories_analyzed": len(repo_authors),
            },
        }

    def calculate_network_metrics(self, network: dict[str, Any]) -> dict[str, Any]:
        """Calculate network analysis metrics."""
        nodes = network["nodes"]
        edges = network["edges"]

        if not nodes:
            return {}

        # Build adjacency list
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[edge["source"]].add(edge["target"])
            adjacency[edge["target"]].add(edge["source"])

        # Calculate degree centrality
        degree_centrality = {}
        for node in nodes:
            node_id = node["id"]
            degree = len(adjacency[node_id])
            # Normalize by max possible connections (n-1)
            degree_centrality[node_id] = degree / (len(nodes) - 1) if len(nodes) > 1 else 0

        # Find most central authors
        top_central = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

        # Calculate network density
        max_edges = (len(nodes) * (len(nodes) - 1)) / 2
        density = len(edges) / max_edges if max_edges > 0 else 0

        # Find most collaborative pairs
        top_collaborations = sorted(
            [(e["source"], e["target"], e["weight"]) for e in edges],
            key=lambda x: x[2],
            reverse=True,
        )[:10]

        return {
            "density": density,
            "average_degree": sum(degree_centrality.values()) / len(nodes) if nodes else 0,
            "top_central_authors": [
                {"author": author, "centrality": float(cent)} for author, cent in top_central
            ],
            "top_collaborations": [
                {"author1": a1, "author2": a2, "shared_repos": w}
                for a1, a2, w in top_collaborations
            ],
            "degree_centrality": {k: float(v) for k, v in degree_centrality.items()},
        }

    def create_network_visualization(self, network_data: dict[str, Any], output_dir: str) -> str:
        """Create interactive network visualization."""
        if not PLOTLY_AVAILABLE:
            return ""

        network = network_data["network"]
        nodes = network["nodes"]
        edges = network["edges"]

        if not nodes:
            return ""

        # Use spring layout algorithm (simple circular for small networks)
        import math

        # Calculate positions
        n = len(nodes)
        positions = {}

        if n <= 10:
            # Circular layout for small networks
            for i, node in enumerate(nodes):
                angle = 2 * math.pi * i / n
                x = math.cos(angle)
                y = math.sin(angle)
                positions[node["id"]] = (x, y)
        else:
            # Grid layout for larger networks
            cols = int(math.ceil(math.sqrt(n)))
            for i, node in enumerate(nodes):
                row = i // cols
                col = i % cols
                positions[node["id"]] = (col, row)

        # Create edge traces
        edge_traces = []
        for edge in edges:
            if edge["source"] in positions and edge["target"] in positions:
                x0, y0 = positions[edge["source"]]
                x1, y1 = positions[edge["target"]]

                # Line width based on weight
                width = min(1 + edge["weight"], 5)

                edge_trace = go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode="lines",
                    line=dict(width=width, color="rgba(125,125,125,0.3)"),
                    hoverinfo="text",
                    text=f"{edge['source']} ↔ {edge['target']}<br>Shared repos: {edge['weight']}",
                    showlegend=False,
                )
                edge_traces.append(edge_trace)

        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []

        for node in nodes:
            if node["id"] in positions:
                x, y = positions[node["id"]]
                node_x.append(x)
                node_y.append(y)

                # Size by commit count
                size = 10 + min(node["commit_count"] / 5, 40)
                node_size.append(size)

                # Color by number of repos
                node_color.append(node["repo_count"])

                # Hover text
                text = (
                    f"<b>{node['id']}</b><br>"
                    f"Commits: {node['commit_count']}<br>"
                    f"Repositories: {node['repo_count']}<br>"
                    f"Repos: {', '.join(node['repos'])}"
                )
                node_text.append(text)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Repositories", thickness=15, len=0.7),
                line=dict(width=2, color="white"),
            ),
            text=[node["id"] for node in nodes if node["id"] in positions],
            textposition="top center",
            textfont=dict(size=10),
            hovertext=node_text,
            hoverinfo="text",
            showlegend=False,
        )

        # Create figure
        fig = go.Figure(
            data=edge_traces + [node_trace],
            layout=go.Layout(
                title="Collaboration Network (from Git Commit History)",
                showlegend=False,
                hovermode="closest",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor="white",
                height=600,
            ),
        )

        output_path = os.path.join(output_dir, "collaboration_network_real.html")
        fig.write_html(output_path)
        return output_path

    def create_author_metrics_chart(self, network_data: dict[str, Any], output_dir: str) -> str:
        """Create visualization of author metrics."""
        if not PLOTLY_AVAILABLE:
            return ""

        metrics = network_data.get("metrics", {})
        top_authors = metrics.get("top_central_authors", [])[:10]

        if not top_authors:
            return ""

        authors = [a["author"] for a in top_authors]
        centrality = [a["centrality"] for a in top_authors]

        fig = go.Figure(
            data=[go.Bar(x=centrality, y=authors, orientation="h", marker_color="lightblue")]
        )

        fig.update_layout(
            title="Most Central Authors (by Network Centrality)",
            xaxis_title="Degree Centrality",
            yaxis_title="Author",
            height=max(400, len(authors) * 40),
        )

        output_path = os.path.join(output_dir, "author_centrality.html")
        fig.write_html(output_path)
        return output_path


def analyze_collaboration_network(
    repos_data: list[dict], org_name: str, github_token: str
) -> dict[str, Any]:
    """Main function to analyze collaboration network."""
    if not PYGITHUB_AVAILABLE:
        print("ERROR: PyGithub not available")
        return {"error": "PyGithub not installed"}

    print("Analyzing collaboration network...")

    analyzer = CollaborationNetworkAnalyzer(github_token)

    # Build network
    network_data = analyzer.build_collaboration_network(repos_data, org_name)

    # Create visualizations
    if PLOTLY_AVAILABLE:
        net_viz = analyzer.create_network_visualization(network_data, "docs/visualizations")
        metrics_viz = analyzer.create_author_metrics_chart(network_data, "docs/visualizations")

        network_data["visualizations"] = {"network": net_viz, "metrics": metrics_viz}

    # Save results
    output_path = "data/collaboration_network.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(network_data, f, indent=2, ensure_ascii=False)

    print(f"Collaboration network saved to {output_path}")
    print(f"  Total authors: {network_data['summary']['total_authors']}")
    print(f"  Total collaborations: {network_data['summary']['total_collaborations']}")
    print(f"  Network density: {network_data['metrics']['density']:.3f}")

    return network_data


def main():
    """Test collaboration network analyzer."""
    print("Collaboration Network Analyzer")
    print("=" * 60)

    if not PYGITHUB_AVAILABLE:
        print("ERROR: PyGithub not available")
        print("Install with: pip install PyGithub")
        return

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("ERROR: GITHUB_TOKEN environment variable not set")
        return

    org_name = os.environ.get("GITHUB_ORG", "Digital-AI-Finance")

    if os.path.exists("data/repos.json"):
        with open("data/repos.json", encoding="utf-8") as f:
            repos_data = json.load(f)

        results = analyze_collaboration_network(repos_data, org_name, github_token)

        if "error" not in results:
            print("\nTop collaborations:")
            for collab in results["metrics"]["top_collaborations"][:5]:
                print(
                    f"  {collab['author1']} ↔ {collab['author2']}: {collab['shared_repos']} shared repos"
                )

    else:
        print("No repos data found. Run build_research_platform.py first.")


if __name__ == "__main__":
    main()
