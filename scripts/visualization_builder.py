#!/usr/bin/env python3
"""
Interactive visualization system using Plotly for research dashboards.
Creates charts, network graphs, and interactive elements.
"""

import json
import os

from viz_footer import inject_footer_into_html

# Note: Plotly is optional - will generate JSON data that can be rendered client-side
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    PLOTLY_AVAILABLE = True
except ImportError:
    print("Plotly not installed. Install with: pip install plotly")
    PLOTLY_AVAILABLE = False

SCRIPT_NAME = "visualization_builder.py"
DATA_SOURCE = "data/repos.json"


class VisualizationBuilder:
    """Build interactive visualizations for research dashboard."""

    def __init__(self, output_dir="docs/visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _write_html_with_footer(self, fig, output_path: str, data_source: str = DATA_SOURCE):
        """Write Plotly figure to HTML and inject generation footer."""
        fig.write_html(output_path)
        with open(output_path, encoding="utf-8") as f:
            html_content = f.read()
        html_content = inject_footer_into_html(html_content, SCRIPT_NAME, data_source)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def create_citation_network(self, citation_graph: dict) -> str:
        """Create interactive citation network visualization."""
        if not PLOTLY_AVAILABLE:
            return self._generate_d3_network_data(citation_graph)

        nodes = citation_graph.get("network", {}).get("nodes", [])
        edges = citation_graph.get("network", {}).get("edges", [])

        if not nodes:
            return ""

        # Create network layout (simple circle for now)
        import math

        n = len(nodes)
        node_positions = {}

        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / n
            x = math.cos(angle)
            y = math.sin(angle)
            node_positions[node["id"]] = (x, y)

        # Create edge traces
        edge_traces = []
        for edge in edges:
            src = edge["source"]
            tgt = edge["target"]

            if src in node_positions and tgt in node_positions:
                x0, y0 = node_positions[src]
                x1, y1 = node_positions[tgt]

                edge_trace = go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode="lines",
                    line={"width": 0.5, "color": "#888"},
                    hoverinfo="none",
                    showlegend=False,
                )
                edge_traces.append(edge_trace)

        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_size = []

        for node in nodes:
            if node["id"] in node_positions:
                x, y = node_positions[node["id"]]
                node_x.append(x)
                node_y.append(y)
                citations = node.get("citations", 0)
                node_text.append(f"{node['id']}<br>Citations: {citations}")
                node_size.append(10 + citations * 2)  # Size by citations

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker={"size": node_size, "color": "#1f77b4", "line": {"width": 2, "color": "white"}},
            text=[node["id"] for node in nodes if node["id"] in node_positions],
            textposition="top center",
            hovertext=node_text,
            hoverinfo="text",
        )

        # Create figure
        fig = go.Figure(
            data=edge_traces + [node_trace],
            layout=go.Layout(
                title="Citation Network",
                showlegend=False,
                hovermode="closest",
                xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
                yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
                plot_bgcolor="white",
            ),
        )

        # Save as HTML
        output_path = os.path.join(self.output_dir, "citation_network.html")
        self._write_html_with_footer(fig, output_path, "data/citation_report.json")

        return output_path

    def create_publication_timeline(self, repos_data: list[dict]) -> str:
        """Create timeline of publications."""
        if not PLOTLY_AVAILABLE:
            return ""

        # Collect publications with years
        pubs_by_year = {}

        for repo in repos_data:
            research_meta = repo.get("research_metadata", {})
            publications = research_meta.get("publications", [])

            for pub in publications:
                year = pub.get("year")
                if year:
                    if year not in pubs_by_year:
                        pubs_by_year[year] = 0
                    pubs_by_year[year] += 1

        if not pubs_by_year:
            return ""

        # Create bar chart
        years = sorted(pubs_by_year.keys())
        counts = [pubs_by_year[year] for year in years]

        fig = go.Figure(data=[go.Bar(x=years, y=counts, marker_color="#1f77b4")])

        fig.update_layout(
            title="Publications Over Time",
            xaxis_title="Year",
            yaxis_title="Number of Publications",
            plot_bgcolor="white",
        )

        output_path = os.path.join(self.output_dir, "publication_timeline.html")
        self._write_html_with_footer(fig, output_path)

        return output_path

    def create_research_impact_chart(self, impact_metrics: dict) -> str:
        """Create research impact visualization."""
        if not PLOTLY_AVAILABLE:
            return ""

        if not impact_metrics:
            return ""

        # Prepare data
        repos = []
        internal_citations = []
        external_citations = []
        h_indices = []

        for repo_name, metrics in impact_metrics.items():
            repos.append(repo_name)
            internal_citations.append(metrics.get("internal_citations", 0))
            external_citations.append(metrics.get("external_citations", 0))
            h_indices.append(metrics.get("h_index", 0))

        # Create subplot with multiple charts
        fig = make_subplots(
            rows=1,
            cols=3,
            subplot_titles=("Internal Citations", "External Citations", "H-Index"),
            specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]],
        )

        fig.add_trace(
            go.Bar(x=repos, y=internal_citations, name="Internal", marker_color="#1f77b4"),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(x=repos, y=external_citations, name="External", marker_color="#ff7f0e"),
            row=1,
            col=2,
        )

        fig.add_trace(
            go.Bar(x=repos, y=h_indices, name="H-Index", marker_color="#2ca02c"), row=1, col=3
        )

        fig.update_layout(title_text="Research Impact Metrics", showlegend=False, height=400)

        output_path = os.path.join(self.output_dir, "research_impact.html")
        self._write_html_with_footer(fig, output_path)

        return output_path

    def create_language_distribution(self, repos_data: list[dict]) -> str:
        """Create language distribution pie chart."""
        if not PLOTLY_AVAILABLE:
            return ""

        languages = {}
        for repo in repos_data:
            lang = repo.get("language", "Unknown")
            languages[lang] = languages.get(lang, 0) + 1

        fig = go.Figure(
            data=[go.Pie(labels=list(languages.keys()), values=list(languages.values()))]
        )

        fig.update_layout(title="Programming Language Distribution")

        output_path = os.path.join(self.output_dir, "language_distribution.html")
        self._write_html_with_footer(fig, output_path)

        return output_path

    def create_collaboration_network(self, repos_data: list[dict]) -> str:
        """Create collaboration network based on shared authors."""
        # Extract authors from all repos
        repo_authors = {}

        for repo in repos_data:
            research_meta = repo.get("research_metadata", {})
            authors = research_meta.get("research", {}).get("authors", [])

            if authors:
                repo_authors[repo["name"]] = {
                    author.get("name", "") for author in authors if author.get("name")
                }

        # Find collaborations (shared authors)
        collaborations = []

        repos = list(repo_authors.keys())
        for i, repo1 in enumerate(repos):
            for repo2 in repos[i + 1 :]:
                shared = repo_authors[repo1] & repo_authors[repo2]
                if shared:
                    collaborations.append(
                        {"source": repo1, "target": repo2, "shared_authors": len(shared)}
                    )

        # Generate network data
        network_data = {
            "nodes": [
                {"id": repo, "authors": len(authors)} for repo, authors in repo_authors.items()
            ],
            "edges": collaborations,
        }

        output_path = os.path.join(self.output_dir, "collaboration_network.json")
        with open(output_path, "w") as f:
            json.dump(network_data, f, indent=2)

        return output_path

    def _generate_d3_network_data(self, citation_graph: dict) -> str:
        """Generate D3.js compatible network data."""
        # Convert to D3 format
        d3_data = {
            "nodes": citation_graph.get("network", {}).get("nodes", []),
            "links": [
                {
                    "source": edge["source"],
                    "target": edge["target"],
                    "type": edge.get("type", "cites"),
                }
                for edge in citation_graph.get("network", {}).get("edges", [])
            ],
        }

        output_path = os.path.join(self.output_dir, "citation_network.json")
        with open(output_path, "w") as f:
            json.dump(d3_data, f, indent=2)

        return output_path


def generate_all_visualizations(
    repos_data: list[dict], citation_report: dict = None
) -> dict[str, str]:
    """Generate all visualizations for dashboard."""
    print("Generating visualizations...")

    builder = VisualizationBuilder()
    viz_paths = {}

    # Language distribution
    lang_path = builder.create_language_distribution(repos_data)
    if lang_path:
        viz_paths["language_distribution"] = lang_path

    # Publication timeline
    timeline_path = builder.create_publication_timeline(repos_data)
    if timeline_path:
        viz_paths["publication_timeline"] = timeline_path

    # If citation report available
    if citation_report:
        # Citation network
        network_path = builder.create_citation_network(citation_report.get("citation_graph", {}))
        if network_path:
            viz_paths["citation_network"] = network_path

        # Research impact
        impact_path = builder.create_research_impact_chart(
            citation_report.get("impact_metrics", {})
        )
        if impact_path:
            viz_paths["research_impact"] = impact_path

    # Collaboration network
    collab_path = builder.create_collaboration_network(repos_data)
    if collab_path:
        viz_paths["collaboration_network"] = collab_path

    print(f"Generated {len(viz_paths)} visualizations")
    return viz_paths


def main():
    """Test visualization builder."""
    print("Visualization Builder")
    print("=" * 60)

    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Install with: pip install plotly")
        return

    # Load data
    if os.path.exists("data/repos.json"):
        with open("data/repos.json") as f:
            repos_data = json.load(f)

        citation_report = None
        if os.path.exists("data/citation_report.json"):
            with open("data/citation_report.json") as f:
                citation_report = json.load(f)

        viz_paths = generate_all_visualizations(repos_data, citation_report)

        print("\nGenerated visualizations:")
        for name, path in viz_paths.items():
            print(f"  - {name}: {path}")

    else:
        print("No repos data found. Run fetch_org_data_research.py first.")


if __name__ == "__main__":
    main()
