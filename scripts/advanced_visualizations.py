#!/usr/bin/env python3
"""
Advanced visualization system with sophisticated Plotly charts.
Includes heatmaps, sunburst charts, treemaps, and animated visualizations.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    print("Plotly not installed. Install with: pip install plotly")
    PLOTLY_AVAILABLE = False


class AdvancedVisualizationBuilder:
    """Build advanced interactive visualizations."""

    def __init__(self, output_dir='docs/visualizations'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_activity_heatmap(self, repos_data: List[Dict]) -> str:
        """Create repository activity heatmap by day of week and hour."""
        if not PLOTLY_AVAILABLE:
            return ""

        # Aggregate activity data (placeholder - would need actual commit data)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = list(range(24))

        # For now, create sample data - in real implementation, parse commit timestamps
        import random
        activity_data = [[random.randint(0, 20) for _ in hours] for _ in days]

        fig = go.Figure(data=go.Heatmap(
            z=activity_data,
            x=hours,
            y=days,
            colorscale='Blues',
            hovertemplate='Day: %{y}<br>Hour: %{x}<br>Commits: %{z}<extra></extra>'
        ))

        fig.update_layout(
            title='Repository Activity Heatmap',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            height=400
        )

        output_path = os.path.join(self.output_dir, 'activity_heatmap.html')
        fig.write_html(output_path)
        return output_path

    def create_topic_sunburst(self, repos_data: List[Dict]) -> str:
        """Create sunburst chart of topics and languages."""
        if not PLOTLY_AVAILABLE:
            return ""

        # Build hierarchical data
        labels = ['All Repositories']
        parents = ['']
        values = [len(repos_data)]
        colors = []

        # Add language layer
        lang_counts = {}
        lang_topics = defaultdict(lambda: defaultdict(int))

        for repo in repos_data:
            lang = repo.get('language', 'Unknown')
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

            topics = repo.get('topics', [])
            for topic in topics[:3]:  # Limit to top 3 topics per repo
                lang_topics[lang][topic] += 1

        # Add languages
        for lang, count in lang_counts.items():
            labels.append(lang)
            parents.append('All Repositories')
            values.append(count)

        # Add topics under languages
        for lang, topics in lang_topics.items():
            for topic, count in topics.items():
                labels.append(f"{topic} ({lang})")
                parents.append(lang)
                values.append(count)

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(
                colorscale='RdBu',
                cmid=len(repos_data)/2
            ),
            hovertemplate='<b>%{label}</b><br>Repositories: %{value}<extra></extra>'
        ))

        fig.update_layout(
            title='Repository Topics and Languages (Sunburst)',
            height=600
        )

        output_path = os.path.join(self.output_dir, 'topic_sunburst.html')
        fig.write_html(output_path)
        return output_path

    def create_reproducibility_radar(self, reproducibility_report: Dict) -> str:
        """Create radar chart showing reproducibility dimensions."""
        if not PLOTLY_AVAILABLE:
            return ""

        repos_summary = reproducibility_report.get('repositories', {})
        if not repos_summary:
            return ""

        # Get top 5 repos by reproducibility score
        top_repos = sorted(
            repos_summary.items(),
            key=lambda x: x[1].get('reproducibility_score', {}).get('score', 0),
            reverse=True
        )[:5]

        categories = ['Documentation', 'Environment', 'Data', 'Code', 'Community']

        fig = go.Figure()

        for repo_name, repo_data in top_repos:
            breakdown = repo_data.get('reproducibility_score', {}).get('breakdown', {})
            scores = [
                breakdown.get('documentation', 0),
                breakdown.get('environment', 0),
                breakdown.get('data', 0),
                breakdown.get('code', 0),
                breakdown.get('community', 0)
            ]

            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=repo_name[:20]  # Truncate long names
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 30]
                )
            ),
            title='Reproducibility Score Breakdown (Top 5 Repositories)',
            height=600,
            showlegend=True
        )

        output_path = os.path.join(self.output_dir, 'reproducibility_radar.html')
        fig.write_html(output_path)
        return output_path

    def create_citation_trend_chart(self, citation_report: Dict) -> str:
        """Create time series of citation growth."""
        if not PLOTLY_AVAILABLE:
            return ""

        growth_trends = citation_report.get('growth_trends', {})
        if not growth_trends:
            return ""

        fig = go.Figure()

        for repo_name, trend_data in growth_trends.items():
            # In real implementation, would have historical snapshots
            # For now, create sample trend
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            current_citations = trend_data.get('current_citations', 0)

            # Simulate growth
            citations = [max(0, current_citations - (5-i)*2) for i in range(6)]

            fig.add_trace(go.Scatter(
                x=months,
                y=citations,
                mode='lines+markers',
                name=repo_name,
                line=dict(width=2),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title='Citation Growth Trends',
            xaxis_title='Month',
            yaxis_title='Total Citations',
            hovermode='x unified',
            height=500
        )

        output_path = os.path.join(self.output_dir, 'citation_trends.html')
        fig.write_html(output_path)
        return output_path

    def create_repository_treemap(self, repos_data: List[Dict]) -> str:
        """Create treemap of repositories sized by various metrics."""
        if not PLOTLY_AVAILABLE:
            return ""

        # Prepare data
        names = []
        parents = []
        values = []
        colors = []
        text = []

        # Group by language
        lang_repos = defaultdict(list)
        for repo in repos_data:
            lang = repo.get('language', 'Unknown')
            lang_repos[lang].append(repo)

        # Add root
        names.append('All Repositories')
        parents.append('')
        values.append(0)  # Will be computed automatically
        colors.append(0)
        text.append('')

        # Add languages
        for lang in lang_repos.keys():
            names.append(lang)
            parents.append('All Repositories')
            values.append(0)
            colors.append(0)
            text.append('')

        # Add repositories
        for lang, repos in lang_repos.items():
            for repo in repos:
                names.append(repo['name'])
                parents.append(lang)

                # Size by lines of code (estimate from size_kb)
                size = repo.get('size_kb', 100)
                values.append(size)

                # Color by stars
                stars = repo.get('stars', 0)
                colors.append(stars)

                text.append(f"{repo['name']}<br>Stars: {stars}<br>Size: {size} KB")

        fig = go.Figure(go.Treemap(
            labels=names,
            parents=parents,
            values=values,
            text=text,
            textposition='middle center',
            marker=dict(
                colors=colors,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Stars")
            ),
            hovertemplate='<b>%{label}</b><br>%{text}<extra></extra>'
        ))

        fig.update_layout(
            title='Repository Size Treemap (sized by KB, colored by stars)',
            height=600
        )

        output_path = os.path.join(self.output_dir, 'repository_treemap.html')
        fig.write_html(output_path)
        return output_path

    def create_metric_comparison_chart(self, repos_data: List[Dict]) -> str:
        """Create parallel coordinates plot for multi-dimensional comparison."""
        if not PLOTLY_AVAILABLE:
            return ""

        # Prepare data for parallel coordinates
        repo_names = []
        stars = []
        forks = []
        sizes = []
        contributors = []

        for repo in repos_data:
            repo_names.append(repo['name'])
            stars.append(repo.get('stars', 0))
            forks.append(repo.get('forks', 0))
            sizes.append(repo.get('size_kb', 0) / 1000)  # Convert to MB
            contributors.append(repo.get('contributors_count', 0))

        fig = go.Figure(data=
            go.Parcoords(
                line=dict(
                    color=stars,
                    colorscale='Viridis',
                    showscale=True,
                    cmin=min(stars) if stars else 0,
                    cmax=max(stars) if stars else 1
                ),
                dimensions=list([
                    dict(range=[0, max(stars) if stars else 1],
                         label='Stars', values=stars),
                    dict(range=[0, max(forks) if forks else 1],
                         label='Forks', values=forks),
                    dict(range=[0, max(sizes) if sizes else 1],
                         label='Size (MB)', values=sizes),
                    dict(range=[0, max(contributors) if contributors else 1],
                         label='Contributors', values=contributors)
                ])
            )
        )

        fig.update_layout(
            title='Repository Metrics Comparison (Parallel Coordinates)',
            height=500
        )

        output_path = os.path.join(self.output_dir, 'metric_comparison.html')
        fig.write_html(output_path)
        return output_path


def generate_advanced_visualizations(repos_data: List[Dict],
                                     citation_report: Dict = None,
                                     reproducibility_report: Dict = None) -> Dict[str, str]:
    """Generate all advanced visualizations."""
    print("Generating advanced visualizations...")

    builder = AdvancedVisualizationBuilder()
    viz_paths = {}

    # Activity heatmap
    heatmap_path = builder.create_activity_heatmap(repos_data)
    if heatmap_path:
        viz_paths['activity_heatmap'] = heatmap_path

    # Topic sunburst
    sunburst_path = builder.create_topic_sunburst(repos_data)
    if sunburst_path:
        viz_paths['topic_sunburst'] = sunburst_path

    # Repository treemap
    treemap_path = builder.create_repository_treemap(repos_data)
    if treemap_path:
        viz_paths['repository_treemap'] = treemap_path

    # Metric comparison
    comparison_path = builder.create_metric_comparison_chart(repos_data)
    if comparison_path:
        viz_paths['metric_comparison'] = comparison_path

    # Reproducibility radar (if data available)
    if reproducibility_report:
        radar_path = builder.create_reproducibility_radar(reproducibility_report)
        if radar_path:
            viz_paths['reproducibility_radar'] = radar_path

    # Citation trends (if data available)
    if citation_report:
        trends_path = builder.create_citation_trend_chart(citation_report)
        if trends_path:
            viz_paths['citation_trends'] = trends_path

    print(f"Generated {len(viz_paths)} advanced visualizations")
    return viz_paths


def main():
    """Test advanced visualization builder."""
    print("Advanced Visualization Builder")
    print("=" * 60)

    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Install with: pip install plotly")
        return

    # Load data
    if os.path.exists('data/repos.json'):
        with open('data/repos.json', 'r', encoding='utf-8') as f:
            repos_data = json.load(f)

        citation_report = None
        if os.path.exists('data/citation_report.json'):
            with open('data/citation_report.json', 'r', encoding='utf-8') as f:
                citation_report = json.load(f)

        reproducibility_report = None
        if os.path.exists('data/reproducibility_report.json'):
            with open('data/reproducibility_report.json', 'r', encoding='utf-8') as f:
                reproducibility_report = json.load(f)

        viz_paths = generate_advanced_visualizations(
            repos_data,
            citation_report,
            reproducibility_report
        )

        print("\nGenerated visualizations:")
        for name, path in viz_paths.items():
            print(f"  - {name}: {path}")

    else:
        print("No repos data found. Run build_research_platform.py first.")


if __name__ == '__main__':
    main()
