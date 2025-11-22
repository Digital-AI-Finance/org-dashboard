#!/usr/bin/env python3
"""
Generate Interactive Repository Overview
Creates a visual, clickable gallery of all repositories
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Warning: plotly not installed. Skipping interactive visualizations.")


def load_repositories(repos_file: str = 'data/repos.json') -> List[Dict[str, Any]]:
    """Load repository data."""
    with open(repos_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_repository_grid_html(repos: List[Dict[str, Any]],
                                  output_path: str = 'docs/visualizations/repository_overview.html') -> str:
    """
    Create interactive HTML grid of repositories.
    """
    # Sort repos by last updated
    sorted_repos = sorted(repos, key=lambda x: x.get('updated_at', ''), reverse=True)

    # Generate HTML
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repository Overview - Digital AI Finance</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .repo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }

        .repo-card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .repo-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .repo-card:hover::before {
            transform: scaleX(1);
        }

        .repo-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .repo-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .repo-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            flex-shrink: 0;
        }

        .repo-icon svg {
            width: 28px;
            height: 28px;
            fill: white;
        }

        .repo-title {
            flex: 1;
        }

        .repo-title h3 {
            font-size: 1.3rem;
            color: #2d3748;
            margin-bottom: 5px;
            word-break: break-word;
        }

        .repo-language {
            display: inline-block;
            padding: 4px 12px;
            background: #f7fafc;
            border-radius: 12px;
            font-size: 0.75rem;
            color: #667eea;
            font-weight: 600;
        }

        .repo-description {
            color: #4a5568;
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 15px 0;
            min-height: 60px;
        }

        .repo-stats {
            display: flex;
            gap: 20px;
            margin: 20px 0;
            padding: 15px 0;
            border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
        }

        .stat {
            display: flex;
            align-items: center;
            gap: 6px;
            color: #718096;
            font-size: 0.9rem;
        }

        .stat svg {
            width: 16px;
            height: 16px;
            fill: currentColor;
        }

        .repo-topics {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
            min-height: 30px;
        }

        .topic-tag {
            padding: 5px 12px;
            background: #edf2f7;
            border-radius: 12px;
            font-size: 0.8rem;
            color: #4a5568;
            transition: all 0.2s ease;
        }

        .topic-tag:hover {
            background: #667eea;
            color: white;
        }

        .repo-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }

        .updated-date {
            font-size: 0.85rem;
            color: #a0aec0;
        }

        .view-button {
            padding: 8px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            border: none;
        }

        .view-button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .filter-bar {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }

        .filter-button {
            padding: 10px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }

        .filter-button:hover, .filter-button.active {
            background: white;
            color: #667eea;
        }

        .search-box {
            margin: 0 auto 30px;
            max-width: 600px;
        }

        .search-box input {
            width: 100%;
            padding: 15px 25px;
            border-radius: 50px;
            border: none;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .repo-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Research Repositories</h1>
            <p>Digital AI Finance Organization</p>
        </div>

        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search repositories...">
        </div>

        <div class="filter-bar">
            <button class="filter-button active" data-filter="all">All ({total})</button>
            <button class="filter-button" data-filter="python">Python</button>
            <button class="filter-button" data-filter="tex">TeX</button>
            <button class="filter-button" data-filter="jupyter">Jupyter</button>
        </div>

        <div class="repo-grid" id="repoGrid">
"""

    # Add repository cards
    for repo in sorted_repos:
        name = repo.get('name', 'Unknown')
        description = repo.get('description', 'No description available')[:150]
        language = repo.get('language', 'Unknown')
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        url = repo.get('html_url', '#')
        topics = repo.get('topics', [])[:5]  # Show max 5 topics
        updated = repo.get('updated_at', '')[:10]  # Just the date

        # Language color coding
        lang_class = language.lower().replace(' ', '-') if language != 'Unknown' else 'unknown'

        html_content += f"""
            <div class="repo-card" data-language="{lang_class}" onclick="window.open('{url}', '_blank')">
                <div class="repo-header">
                    <div class="repo-icon">
                        <svg viewBox="0 0 16 16">
                            <path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
                        </svg>
                    </div>
                    <div class="repo-title">
                        <h3>{name}</h3>
                        <span class="repo-language">{language}</span>
                    </div>
                </div>

                <p class="repo-description">{description}</p>

                <div class="repo-stats">
                    <div class="stat">
                        <svg viewBox="0 0 16 16">
                            <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
                        </svg>
                        {stars}
                    </div>
                    <div class="stat">
                        <svg viewBox="0 0 16 16">
                            <path d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"/>
                        </svg>
                        {forks}
                    </div>
                </div>

                <div class="repo-topics">
"""

        for topic in topics:
            html_content += f'                    <span class="topic-tag">{topic}</span>\n'

        html_content += f"""                </div>

                <div class="repo-footer">
                    <span class="updated-date">Updated {updated}</span>
                    <button class="view-button">View Repo</button>
                </div>
            </div>
"""

    html_content += """        </div>
    </div>

    <script>
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const repoCards = document.querySelectorAll('.repo-card');

        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();

            repoCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });

        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-button');

        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');

                const filter = this.getAttribute('data-filter');

                repoCards.forEach(card => {
                    if (filter === 'all') {
                        card.style.display = 'block';
                    } else {
                        const language = card.getAttribute('data-language');
                        if (language.includes(filter)) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        });
    </script>
</body>
</html>"""

    # Replace total count
    html_content = html_content.replace('{total}', str(len(repos)))

    # Save HTML
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Repository overview saved to: {output_path}")
    return output_path


def create_interactive_network(repos: List[Dict[str, Any]],
                                 output_path: str = 'docs/visualizations/repository_network.html') -> str:
    """
    Create interactive network visualization of repositories.
    """
    if not PLOTLY_AVAILABLE:
        return ""

    import networkx as nx

    # Create network graph
    G = nx.Graph()

    # Add nodes for repositories
    for repo in repos:
        G.add_node(repo['name'],
                   description=repo.get('description', '')[:100],
                   language=repo.get('language', 'Unknown'),
                   stars=repo.get('stargazers_count', 0),
                   url=repo.get('html_url', ''))

    # Add edges based on shared topics
    for i, repo1 in enumerate(repos):
        topics1 = set(repo1.get('topics', []))
        for repo2 in repos[i+1:]:
            topics2 = set(repo2.get('topics', []))
            common_topics = topics1.intersection(topics2)
            if common_topics:
                G.add_edge(repo1['name'], repo2['name'],
                          weight=len(common_topics),
                          topics=list(common_topics))

    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Create edges
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=edge[2]['weight'], color='#ddd'),
            hoverinfo='text',
            text=f"Shared topics: {', '.join(edge[2]['topics'])}",
            showlegend=False
        )
        edge_traces.append(edge_trace)

    # Create nodes
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []
    node_urls = []

    lang_colors = {
        'Python': '#3572A5',
        'Jupyter Notebook': '#DA5B0B',
        'TeX': '#3D6117',
        'Unknown': '#888888'
    }

    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)

        data = node[1]
        node_text.append(f"<b>{node[0]}</b><br>{data['description']}<br>"
                        f"Language: {data['language']}<br>"
                        f"Stars: {data['stars']}")

        node_colors.append(lang_colors.get(data['language'], lang_colors['Unknown']))
        node_sizes.append(20 + data['stars'] * 2)
        node_urls.append(data['url'])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[node[0] for node in G.nodes()],
        textposition='top center',
        hovertext=node_text,
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        customdata=node_urls,
        showlegend=False
    )

    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])

    fig.update_layout(
        title={
            'text': 'Repository Network - Connected by Shared Topics',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2d3748'}
        },
        showlegend=False,
        hovermode='closest',
        margin=dict(l=0, r=0, t=80, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=700
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path, config={'displayModeBar': True, 'displaylogo': False})

    print(f"Repository network saved to: {output_path}")
    return output_path


def main():
    """Main execution function."""
    print("Repository Overview Generator")
    print("=" * 60)

    # Load repositories
    repos = load_repositories()
    print(f"Loaded {len(repos)} repositories")

    # Create visualizations
    visualizations = {}

    print("\nGenerating repository overview...")
    grid_path = create_repository_grid_html(repos)
    visualizations['grid'] = grid_path

    if PLOTLY_AVAILABLE:
        print("Generating network visualization...")
        network_path = create_interactive_network(repos)
        visualizations['network'] = network_path

    print("\n" + "=" * 60)
    print("Generated visualizations:")
    for name, path in visualizations.items():
        print(f"  - {name}: {path}")

    return visualizations


if __name__ == '__main__':
    main()
