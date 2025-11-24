#!/usr/bin/env python3
"""
Create interactive landing page visualization from ML topic analysis.
Generates 3D bubble chart showing discovered research topics.
"""

import json
import os
from typing import Any

from viz_footer import inject_footer_into_html

try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    print("Plotly not installed. Install with: pip install plotly")
    PLOTLY_AVAILABLE = False

SCRIPT_NAME = "create_landing_page_viz.py"
DATA_SOURCE = "data/ml_topic_analysis.json"


def create_topic_bubble_chart(
    topic_analysis: dict[str, Any],
    method="nmf",
    output_path="docs/visualizations/landing_topic_bubbles.html",
) -> str:
    """
    Create interactive 3D bubble chart for landing page.

    Args:
        topic_analysis: ML topic analysis results
        method: 'nmf' or 'lda'
        output_path: Where to save the HTML file
    """
    if not PLOTLY_AVAILABLE:
        print("ERROR: Plotly not available")
        return ""

    method_data = topic_analysis.get("methods", {}).get(method, {})
    topics = method_data.get("topics", [])
    repo_topics = method_data.get("repository_topics", [])

    if not topics:
        print(f"No topics found for {method}")
        return ""

    # Prepare bubble data
    bubble_data = []

    for topic in topics:
        topic_id = topic["topic_id"]

        # Count repositories assigned to this topic
        repo_count = sum(1 for rt in repo_topics if rt["dominant_topic"] == topic_id)

        # Get top keywords
        top_words = topic["words"][:5]
        weights = topic["weights"][:5]

        # Create hover text
        hover_text = f"<b>{topic['label']}</b><br><br>"
        hover_text += "Top Keywords:<br>"
        for word, weight in zip(top_words, weights):
            hover_text += f"  • {word}: {weight:.3f}<br>"
        hover_text += f"<br>Repositories: {repo_count}"

        # Get repository names for this topic
        topic_repos = [rt["repository"] for rt in repo_topics if rt["dominant_topic"] == topic_id]
        if topic_repos:
            hover_text += "<br><br>Repos:<br>" + "<br>".join(f"  - {r}" for r in topic_repos[:5])

        bubble_data.append(
            {
                "topic_id": topic_id,
                "label": topic["label"],
                "repo_count": repo_count,
                "top_words": top_words,
                "hover_text": hover_text,
                "x": topic_id * 1.5,  # Simple spacing
                "y": repo_count,
                "z": sum(weights[:3]),  # Use weight sum for z-axis
            }
        )

    # Determine colors based on keywords (simple categorization)
    colors = []
    for bubble in bubble_data:
        keywords_str = " ".join(bubble["top_words"]).lower()

        # Categorize by domain
        if any(word in keywords_str for word in ["finance", "trading", "market", "portfolio"]):
            colors.append("#1f77b4")  # Blue - Finance
        elif any(word in keywords_str for word in ["machine", "learning", "neural", "ai"]):
            colors.append("#ff7f0e")  # Orange - ML/AI
        elif any(word in keywords_str for word in ["course", "pedagogy", "week", "curriculum"]):
            colors.append("#2ca02c")  # Green - Education
        elif any(word in keywords_str for word in ["data", "analysis", "research"]):
            colors.append("#d62728")  # Red - Research
        else:
            colors.append("#9467bd")  # Purple - Other

    # Create 3D scatter plot
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=[b["x"] for b in bubble_data],
                y=[b["y"] for b in bubble_data],
                z=[b["z"] for b in bubble_data],
                mode="markers+text",
                marker={
                    "size": [max(15, b["repo_count"] * 20) for b in bubble_data],
                    "color": colors,
                    "opacity": 0.8,
                    "line": {"color": "white", "width": 2},
                },
                text=[b["label"] for b in bubble_data],
                textposition="top center",
                textfont={"size": 10, "color": "black"},
                hovertext=[b["hover_text"] for b in bubble_data],
                hoverinfo="text",
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title={
            "text": f"Research Topics Discovery<br><sub>ML Method: {method.upper()} | {len(topics)} Topics Found</sub>",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24, "color": "#3f51b5"},
        },
        scene={
            "xaxis": {"title": "Topic Space", "showgrid": True, "gridcolor": "lightgray"},
            "yaxis": {"title": "Repository Count", "showgrid": True, "gridcolor": "lightgray"},
            "zaxis": {"title": "Topic Strength", "showgrid": True, "gridcolor": "lightgray"},
            "camera": {"eye": {"x": 1.5, "y": 1.5, "z": 1.3}},
            "bgcolor": "rgba(240, 240, 250, 0.5)",
        },
        showlegend=False,
        hovermode="closest",
        height=600,
        margin={"l": 0, "r": 0, "t": 80, "b": 0},
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # Add annotations for categories
    annotations_text = "Color Key: 🔵 Finance | 🟠 ML/AI | 🟢 Education | 🔴 Research | 🟣 Other"
    fig.add_annotation(
        text=annotations_text,
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.05,
        showarrow=False,
        font={"size": 11, "color": "gray"},
        xanchor="center",
    )

    # Save to HTML
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path, config={"displayModeBar": True, "displaylogo": False})

    # Inject generation footer
    with open(output_path, encoding="utf-8") as f:
        html_content = f.read()
    html_content = inject_footer_into_html(html_content, SCRIPT_NAME, DATA_SOURCE)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Landing page visualization saved to: {output_path}")
    return output_path


def create_2d_bubble_chart(
    topic_analysis: dict[str, Any],
    method="nmf",
    output_path="docs/visualizations/landing_topic_bubbles_2d.html",
) -> str:
    """
    Create simpler 2D bubble chart as alternative.
    """
    if not PLOTLY_AVAILABLE:
        return ""

    method_data = topic_analysis.get("methods", {}).get(method, {})
    topics = method_data.get("topics", [])
    repo_topics = method_data.get("repository_topics", [])

    if not topics:
        return ""

    # Prepare data
    labels = []
    sizes = []
    hover_texts = []
    colors_list = []

    for topic in topics:
        topic_id = topic["topic_id"]
        repo_count = sum(1 for rt in repo_topics if rt["dominant_topic"] == topic_id)

        labels.append(topic["label"])
        sizes.append(max(1, repo_count))

        # Hover text
        hover_text = f"<b>{topic['label']}</b><br>"
        hover_text += f"Keywords: {', '.join(topic['words'][:5])}<br>"
        hover_text += f"Repositories: {repo_count}"
        hover_texts.append(hover_text)

        # Color by domain
        keywords_str = " ".join(topic["words"]).lower()
        if "finance" in keywords_str or "trading" in keywords_str:
            colors_list.append("Finance")
        elif "machine" in keywords_str or "learning" in keywords_str:
            colors_list.append("ML/AI")
        elif "course" in keywords_str or "pedagogy" in keywords_str:
            colors_list.append("Education")
        else:
            colors_list.append("Research")

    # Create bubble chart
    fig = px.scatter(
        x=list(range(len(labels))),
        y=sizes,
        size=sizes,
        color=colors_list,
        hover_name=labels,
        text=labels,
        size_max=60,
        color_discrete_map={
            "Finance": "#1f77b4",
            "ML/AI": "#ff7f0e",
            "Education": "#2ca02c",
            "Research": "#d62728",
        },
    )

    fig.update_traces(textposition="top center", hovertext=hover_texts, hoverinfo="text")

    fig.update_layout(
        title=f"Research Topics Overview ({method.upper()})",
        xaxis={"title": "", "showticklabels": False, "showgrid": False},
        yaxis={"title": "Repository Count"},
        height=500,
        showlegend=True,
        legend_title_text="Domain",
        hovermode="closest",
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path, config={"displayModeBar": True, "displaylogo": False})

    # Inject generation footer
    with open(output_path, encoding="utf-8") as f:
        html_content = f.read()
    html_content = inject_footer_into_html(html_content, SCRIPT_NAME, DATA_SOURCE)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"2D bubble chart saved to: {output_path}")
    return output_path


def generate_landing_visualizations(
    topic_analysis_path="data/ml_topic_analysis.json",
) -> dict[str, str]:
    """
    Generate all landing page visualizations.
    """
    print("Generating landing page visualizations...")

    if not os.path.exists(topic_analysis_path):
        print(f"ERROR: {topic_analysis_path} not found")
        print("Run ML topic modeling first: python scripts/ml_topic_modeling.py")
        return {}

    with open(topic_analysis_path, encoding="utf-8") as f:
        topic_analysis = json.load(f)

    viz_paths = {}

    # Create 3D bubble chart (NMF)
    if "nmf" in topic_analysis.get("methods", {}):
        path_3d_nmf = create_topic_bubble_chart(topic_analysis, method="nmf")
        if path_3d_nmf:
            viz_paths["3d_nmf"] = path_3d_nmf

        # Also create 2D version
        path_2d_nmf = create_2d_bubble_chart(topic_analysis, method="nmf")
        if path_2d_nmf:
            viz_paths["2d_nmf"] = path_2d_nmf

    # Create for LDA too
    if "lda" in topic_analysis.get("methods", {}):
        path_3d_lda = create_topic_bubble_chart(
            topic_analysis,
            method="lda",
            output_path="docs/visualizations/landing_topic_bubbles_lda.html",
        )
        if path_3d_lda:
            viz_paths["3d_lda"] = path_3d_lda

        path_2d_lda = create_2d_bubble_chart(
            topic_analysis,
            method="lda",
            output_path="docs/visualizations/landing_topic_bubbles_2d_lda.html",
        )
        if path_2d_lda:
            viz_paths["2d_lda"] = path_2d_lda

    print(f"Generated {len(viz_paths)} landing page visualizations")
    return viz_paths


def main():
    """Test landing page visualization generation."""
    print("Landing Page Visualization Generator")
    print("=" * 60)

    if not PLOTLY_AVAILABLE:
        print("ERROR: Plotly not available")
        return

    viz_paths = generate_landing_visualizations()

    if viz_paths:
        print("\nGenerated visualizations:")
        for name, path in viz_paths.items():
            print(f"  - {name}: {path}")
    else:
        print("No visualizations generated")


if __name__ == "__main__":
    main()
