"""Generate interactive dependency tree visualizations.

Creates Plotly treemap and sunburst charts showing package dependencies
across repositories, highlighting shared dependencies and ecosystem clusters.
"""

import json
import sys
from pathlib import Path

import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.research_platform.analyzers.dependency_analyzer import DependencyAnalyzer
from src.research_platform.models.repository import Repository


def load_repositories(repos_file: Path = Path("data/repos.json")) -> list[Repository]:
    """Load repository data from JSON file."""
    if not repos_file.exists():
        raise FileNotFoundError(f"Repository data not found: {repos_file}")

    with open(repos_file, encoding="utf-8") as f:
        repos_data = json.load(f)

    return [Repository.from_dict(repo_data) for repo_data in repos_data]


def create_dependency_treemap(analysis: dict, output_path: Path) -> None:
    """
    Create interactive treemap showing dependency hierarchy.

    Args:
        analysis: Dependency analysis dictionary from DependencyAnalyzer
        output_path: Path to save HTML file
    """
    # Build hierarchical data for treemap
    labels = ["All Dependencies"]
    parents = [""]
    values = [analysis["total_dependencies"]]
    colors = [0]  # Root node color
    hover_texts = [
        f"Total: {analysis['total_dependencies']} dependencies<br>"
        f"Unique packages: {analysis['total_unique_packages']}<br>"
        f"Repositories: {analysis['total_repositories']}"
    ]

    # Add top-level categories by usage count
    shared_deps = analysis.get("shared_dependencies", {})
    most_common = analysis.get("most_common_packages", [])

    # Category: Shared Dependencies (used by 2+ repos)
    if shared_deps:
        labels.append("Shared Dependencies")
        parents.append("All Dependencies")
        shared_count = sum(shared_deps.values())
        values.append(shared_count)
        colors.append(2)
        hover_texts.append(
            f"Packages shared across multiple repos<br>"
            f"Count: {len(shared_deps)} packages<br>"
            f"Total usage: {shared_count}"
        )

        # Add individual shared packages
        for pkg, count in sorted(shared_deps.items(), key=lambda x: x[1], reverse=True)[:20]:
            labels.append(f"{pkg}")
            parents.append("Shared Dependencies")
            values.append(count)
            colors.append(count)
            hover_texts.append(f"Package: {pkg}<br>Used by {count} repositories")

    # Category: Unique Dependencies (used by 1 repo)
    unique_deps = [(pkg, count) for pkg, count in most_common if count == 1]
    if unique_deps:
        labels.append("Unique Dependencies")
        parents.append("All Dependencies")
        unique_count = len(unique_deps)
        values.append(unique_count)
        colors.append(1)
        hover_texts.append(
            f"Packages used by only one repository<br>" f"Count: {unique_count} packages"
        )

        # Add sample unique packages (limit to 15)
        for pkg, _count in unique_deps[:15]:
            labels.append(f"{pkg}")
            parents.append("Unique Dependencies")
            values.append(1)
            colors.append(1)
            hover_texts.append(f"Package: {pkg}<br>Used by 1 repository")

    # Create treemap
    fig = go.Figure(
        go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            marker={
                "colorscale": "Blues",
                "cmid": 2,
                "colorbar": {"title": "Usage Count"},
                "line": {"width": 2, "color": "white"},
            },
            text=hover_texts,
            hovertemplate="<b>%{label}</b><br>%{text}<extra></extra>",
            textposition="middle center",
        )
    )

    fig.update_layout(
        title={
            "text": "Dependency Tree Map - Package Usage Across Repositories",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        height=800,
        margin={"l": 0, "r": 0, "t": 60, "b": 0},
    )

    # Save HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Dependency treemap saved to {output_path}")


def create_dependency_sunburst(analysis: dict, output_path: Path) -> None:
    """
    Create interactive sunburst chart showing dependency ecosystem.

    Args:
        analysis: Dependency analysis dictionary
        output_path: Path to save HTML file
    """
    # Build hierarchical data
    labels = ["Dependencies"]
    parents = [""]
    values = [analysis["total_dependencies"]]
    colors = ["#003366"]  # Navy blue for root

    most_common = analysis.get("most_common_packages", [])

    # Group by usage frequency
    high_usage = [(pkg, count) for pkg, count in most_common if count >= 3]
    medium_usage = [(pkg, count) for pkg, count in most_common if count == 2]
    low_usage = [(pkg, count) for pkg, count in most_common if count == 1]

    # High usage tier
    if high_usage:
        labels.append("Core Packages (3+ repos)")
        parents.append("Dependencies")
        values.append(sum(c for _, c in high_usage))
        colors.append("#1f77b4")

        for pkg, count in high_usage[:10]:
            labels.append(f"{pkg} ({count})")
            parents.append("Core Packages (3+ repos)")
            values.append(count)
            colors.append("#4da6ff")

    # Medium usage tier
    if medium_usage:
        labels.append("Shared Packages (2 repos)")
        parents.append("Dependencies")
        values.append(sum(c for _, c in medium_usage))
        colors.append("#ff7f0e")

        for pkg, count in medium_usage[:15]:
            labels.append(f"{pkg} ({count})")
            parents.append("Shared Packages (2 repos)")
            values.append(count)
            colors.append("#ffb366")

    # Low usage tier
    if low_usage:
        labels.append("Unique Packages (1 repo)")
        parents.append("Dependencies")
        values.append(len(low_usage))
        colors.append("#2ca02c")

        for pkg, _count in low_usage[:20]:
            labels.append(f"{pkg}")
            parents.append("Unique Packages (1 repo)")
            values.append(1)
            colors.append("#90ee90")

    # Create sunburst
    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker={
                "colors": colors,
                "line": {"width": 2, "color": "white"},
            },
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
            branchvalues="total",
        )
    )

    fig.update_layout(
        title={
            "text": "Dependency Ecosystem - Package Distribution by Usage Tier",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        height=800,
        margin={"l": 0, "r": 0, "t": 60, "b": 0},
    )

    # Save HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Dependency sunburst saved to {output_path}")


def create_dependency_network(
    analysis: dict, analyzer: DependencyAnalyzer, output_path: Path
) -> None:
    """
    Create interactive network graph showing repository-package relationships.

    Args:
        analysis: Dependency analysis dictionary
        analyzer: DependencyAnalyzer instance with built graph
        output_path: Path to save HTML file
    """
    import networkx as nx

    # Extract graph
    G = analyzer.graph

    if G.number_of_nodes() == 0:
        print("No dependency data available for network visualization")
        return

    # Prepare data for Plotly
    # Use spring layout for positioning
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line={"width": 1, "color": "#888"},
        hoverinfo="none",
        mode="lines",
    )

    # Create node traces (repositories vs packages)
    repo_x = []
    repo_y = []
    repo_text = []
    pkg_x = []
    pkg_y = []
    pkg_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_type = G.nodes[node].get("node_type", "package")

        if node_type == "repository":
            repo_x.append(x)
            repo_y.append(y)
            # Count dependencies
            dep_count = G.out_degree(node)
            repo_text.append(f"<b>{node}</b><br>Dependencies: {dep_count}")
        else:
            pkg_x.append(x)
            pkg_y.append(y)
            # Count repos using this package
            repo_count = G.in_degree(node)
            pkg_text.append(f"<b>{node}</b><br>Used by {repo_count} repo(s)")

    # Repository nodes (larger, navy blue)
    repo_trace = go.Scatter(
        x=repo_x,
        y=repo_y,
        mode="markers+text",
        hoverinfo="text",
        text=[t.split("<br>")[0].replace("<b>", "").replace("</b>", "") for t in repo_text],
        hovertext=repo_text,
        textposition="top center",
        marker={
            "size": 20,
            "color": "#003366",
            "line": {"width": 2, "color": "white"},
        },
        name="Repositories",
    )

    # Package nodes (smaller, colored by usage)
    pkg_trace = go.Scatter(
        x=pkg_x,
        y=pkg_y,
        mode="markers",
        hoverinfo="text",
        hovertext=pkg_text,
        marker={
            "size": 10,
            "color": "#1f77b4",
            "line": {"width": 1, "color": "white"},
        },
        name="Packages",
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, pkg_trace, repo_trace])

    fig.update_layout(
        title={
            "text": f"Dependency Network - {analysis['total_repositories']} Repositories, "
            f"{analysis['total_unique_packages']} Packages",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18},
        },
        showlegend=True,
        hovermode="closest",
        height=800,
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        margin={"l": 0, "r": 0, "t": 60, "b": 0},
        plot_bgcolor="white",
    )

    # Save HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Dependency network saved to {output_path}")


def main():
    """Generate all dependency visualizations."""
    print("=" * 60)
    print("Dependency Tree Visualization Generator")
    print("=" * 60)

    # Load data
    print("\nLoading repository data...")
    repositories = load_repositories()
    print(f"Loaded {len(repositories)} repositories")

    # Analyze dependencies
    print("\nAnalyzing dependency patterns...")
    analyzer = DependencyAnalyzer()
    analysis = analyzer.analyze_dependency_patterns(repositories)

    print(f"  - Total unique packages: {analysis['total_unique_packages']}")
    print(f"  - Total dependencies: {analysis['total_dependencies']}")
    print(f"  - Shared packages: {len(analysis.get('shared_dependencies', {}))}")
    print(f"  - Network nodes: {analysis['network_stats']['nodes']}")
    print(f"  - Network edges: {analysis['network_stats']['edges']}")

    # Create visualizations
    print("\nGenerating visualizations...")

    # Treemap
    treemap_path = Path("docs/visualizations/dependency_treemap.html")
    create_dependency_treemap(analysis, treemap_path)

    # Sunburst
    sunburst_path = Path("docs/visualizations/dependency_sunburst.html")
    create_dependency_sunburst(analysis, sunburst_path)

    # Network
    network_path = Path("docs/visualizations/dependency_network_full.html")
    create_dependency_network(analysis, analyzer, network_path)

    print("\n" + "=" * 60)
    print("Dependency visualizations generated successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  - {treemap_path}")
    print(f"  - {sunburst_path}")
    print(f"  - {network_path}")


if __name__ == "__main__":
    main()
