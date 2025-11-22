"""Visualization generator using Plotly."""

import logging
from pathlib import Path
from typing import Any

import plotly.graph_objects as go

from .base import BaseGenerator


class VisualizationGenerator(BaseGenerator):
    """Generate interactive Plotly visualizations."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)

    async def generate(self, data: dict[str, Any], output_path: Path) -> Path:
        """
        Generate Plotly visualization.

        Args:
            data: Visualization data and configuration
            output_path: Output HTML file path

        Returns:
            Path to generated file
        """
        viz_type = data.get("type", "scatter")

        try:
            if viz_type == "scatter":
                fig = self._create_scatter(data)
            elif viz_type == "bar":
                fig = self._create_bar(data)
            elif viz_type == "network":
                fig = self._create_network(data)
            else:
                raise ValueError(f"Unknown visualization type: {viz_type}")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save HTML
            fig.write_html(
                str(output_path),
                config={"displayModeBar": True, "displaylogo": False},
            )

            self.logger.info(f"Generated visualization: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate visualization: {e}")
            raise

    def _create_scatter(self, data: dict[str, Any]) -> go.Figure:
        """Create scatter plot."""
        fig = go.Figure(
            data=go.Scatter(
                x=data.get("x", []),
                y=data.get("y", []),
                mode="markers",
                marker={"size": 10, "color": data.get("colors", "blue")},
                text=data.get("text", []),
                hoverinfo="text",
            )
        )

        fig.update_layout(title=data.get("title", "Scatter Plot"), height=data.get("height", 600))

        return fig

    def _create_bar(self, data: dict[str, Any]) -> go.Figure:
        """Create bar chart."""
        fig = go.Figure(
            data=go.Bar(
                x=data.get("x", []),
                y=data.get("y", []),
                text=data.get("text", []),
                hoverinfo="text",
            )
        )

        fig.update_layout(title=data.get("title", "Bar Chart"), height=data.get("height", 600))

        return fig

    def _create_network(self, data: dict[str, Any]) -> go.Figure:
        """Create network graph."""
        # Simplified network visualization
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])

        # Create edge traces
        edge_traces = []
        for edge in edges:
            x0, y0 = edge["source_pos"]
            x1, y1 = edge["target_pos"]

            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                line={"width": 1, "color": "#ddd"},
                hoverinfo="none",
                showlegend=False,
            )
            edge_traces.append(edge_trace)

        # Create node trace
        node_trace = go.Scatter(
            x=[n["pos"][0] for n in nodes],
            y=[n["pos"][1] for n in nodes],
            mode="markers+text",
            marker={"size": 20, "color": "blue"},
            text=[n["name"] for n in nodes],
            textposition="top center",
            hoverinfo="text",
        )

        fig = go.Figure(data=edge_traces + [node_trace])
        fig.update_layout(
            title=data.get("title", "Network Graph"),
            showlegend=False,
            hovermode="closest",
            height=700,
        )

        return fig

    async def validate_output(self, output_path: Path) -> bool:
        """Validate generated HTML file."""
        return output_path.exists() and output_path.stat().st_size > 1000
