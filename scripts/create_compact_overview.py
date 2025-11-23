#!/usr/bin/env python3
"""
Create compact, content-focused repository overview.
Optimized for information density and research content discovery.
"""

import json
from typing import Dict, List, Any


def load_repos() -> List[Dict[str, Any]]:
    """Load repository data."""
    with open('data/repos.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def categorize_repo(repo: Dict[str, Any]) -> str:
    """Content-based categorization."""
    text = f"{repo.get('name', '')} {repo.get('description', '')} {' '.join(repo.get('topics', []))}".lower()

    if any(k in text for k in ['dashboard', 'automated', 'monitoring', 'platform']):
        return 'tools'
    if any(k in text for k in ['course', 'curriculum', 'pedagogy', 'academic', 'slides']):
        return 'education'
    if any(k in text for k in ['machine-learning', 'neural', 'reinforcement', 'prediction', 'ml', 'ai']):
        return 'ml-ai'
    if any(k in text for k in ['finance', 'trading', 'portfolio', 'risk', 'market']):
        return 'finance'
    return 'other'


def create_compact_overview(repos: List[Dict[str, Any]],
                             output_path: str = 'docs/visualizations/repository_overview_compact.html') -> str:
    """Create compact, content-dense repository overview."""

    # Sort and categorize
    sorted_repos = sorted(repos, key=lambda x: x.get('updated_at', ''), reverse=True)

    # Count categories
    cats = {}
    for r in sorted_repos:
        cat = categorize_repo(r)
        cats[cat] = cats.get(cat, 0) + 1

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repository Research Overview</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: #f8f9fa;
            padding: 20px;
            line-height: 1.5;
        }}

        .header {{
            background: white;
            padding: 20px 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 1.75rem;
            color: #1a202c;
            margin-bottom: 5px;
        }}

        .header p {{
            color: #718096;
            font-size: 0.95rem;
        }}

        .controls {{
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .search-box {{
            flex: 1;
            min-width: 250px;
        }}

        .search-box input {{
            width: 100%;
            padding: 8px 15px;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-size: 0.9rem;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #4299e1;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }}

        .filters {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 6px 14px;
            border: 1px solid #cbd5e0;
            background: white;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
            color: #4a5568;
            font-weight: 500;
        }}

        .filter-btn:hover {{
            border-color: #4299e1;
            color: #2b6cb0;
            background: #ebf8ff;
        }}

        .filter-btn.active {{
            background: #4299e1;
            color: white;
            border-color: #4299e1;
        }}

        .repo-grid {{
            display: grid;
            gap: 12px;
        }}

        .repo-card {{
            background: white;
            padding: 16px 20px;
            border-radius: 6px;
            border-left: 3px solid #cbd5e0;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}

        .repo-card:hover {{
            border-left-color: #4299e1;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transform: translateX(2px);
        }}

        .repo-card[data-category="finance"] {{ border-left-color: #48bb78; }}
        .repo-card[data-category="ml-ai"] {{ border-left-color: #ed8936; }}
        .repo-card[data-category="education"] {{ border-left-color: #4299e1; }}
        .repo-card[data-category="tools"] {{ border-left-color: #9f7aea; }}

        .repo-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }}

        .repo-title {{
            flex: 1;
        }}

        .repo-title h3 {{
            font-size: 1.1rem;
            color: #2d3748;
            margin-bottom: 4px;
            font-weight: 600;
        }}

        .repo-meta {{
            display: flex;
            gap: 12px;
            font-size: 0.8rem;
            color: #718096;
            margin-bottom: 8px;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .badge {{
            display: inline-block;
            padding: 2px 8px;
            background: #edf2f7;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            color: #4a5568;
        }}

        .badge.finance {{ background: #c6f6d5; color: #22543d; }}
        .badge.ml-ai {{ background: #fed7d7; color: #742a2a; }}
        .badge.education {{ background: #bee3f8; color: #2c5282; }}
        .badge.tools {{ background: #e9d8fd; color: #44337a; }}

        .repo-description {{
            color: #4a5568;
            font-size: 0.9rem;
            margin-bottom: 10px;
            line-height: 1.5;
        }}

        .repo-topics {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 8px;
        }}

        .topic {{
            padding: 3px 10px;
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            font-size: 0.75rem;
            color: #2d3748;
        }}

        .topic:hover {{
            background: #edf2f7;
            border-color: #cbd5e0;
        }}

        .repo-stats {{
            display: flex;
            gap: 16px;
            font-size: 0.8rem;
            color: #a0aec0;
            padding-top: 8px;
            border-top: 1px solid #f7fafc;
        }}

        .stat {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .stat strong {{
            color: #4a5568;
            font-weight: 600;
        }}

        .count {{
            background: #edf2f7;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #2d3748;
        }}

        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.5rem; }}
            .controls {{ flex-direction: column; }}
            .search-box {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Research Repository Catalog</h1>
        <p>Digital AI Finance · {len(repos)} repositories</p>
    </div>

    <div class="controls">
        <div class="search-box">
            <input type="text" id="search" placeholder="Search by name, description, or topics...">
        </div>
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All <span class="count">{len(repos)}</span></button>
            <button class="filter-btn" data-filter="finance">Finance <span class="count">{cats.get('finance', 0)}</span></button>
            <button class="filter-btn" data-filter="ml-ai">ML/AI <span class="count">{cats.get('ml-ai', 0)}</span></button>
            <button class="filter-btn" data-filter="education">Education <span class="count">{cats.get('education', 0)}</span></button>
            <button class="filter-btn" data-filter="tools">Tools <span class="count">{cats.get('tools', 0)}</span></button>
        </div>
    </div>

    <div class="repo-grid">"""

    # Generate compact cards
    for repo in sorted_repos:
        name = repo.get('name', 'Unknown')
        desc = repo.get('description', 'No description')
        url = repo.get('url', '#')
        topics = repo.get('topics', [])[:6]
        stars = repo.get('stars', 0)
        forks = repo.get('forks', 0)
        updated = repo.get('updated_at', '')[:10]
        lang = repo.get('language', 'Unknown')

        cat = categorize_repo(repo)
        cat_labels = {
            'finance': 'Finance',
            'ml-ai': 'ML/AI',
            'education': 'Education',
            'tools': 'Tools',
            'other': 'Other'
        }
        cat_label = cat_labels.get(cat, 'Other')

        topics_html = ''.join(f'<span class="topic">{t}</span>' for t in topics)

        html += f"""
        <div class="repo-card" data-category="{cat}" data-search="{name.lower()} {desc.lower()} {' '.join(topics).lower()}" onclick="window.open('{url}', '_blank')">
            <div class="repo-header">
                <div class="repo-title">
                    <h3>{name}</h3>
                    <div class="repo-meta">
                        <span class="badge {cat}">{cat_label}</span>
                        <span class="meta-item">{lang}</span>
                        <span class="meta-item">Updated {updated}</span>
                    </div>
                </div>
            </div>

            <div class="repo-description">{desc}</div>

            <div class="repo-topics">{topics_html}</div>

            <div class="repo-stats">
                <div class="stat"><strong>Stars:</strong> {stars}</div>
                <div class="stat"><strong>Forks:</strong> {forks}</div>
                <div class="stat"><strong>Topics:</strong> {len(repo.get('topics', []))}</div>
            </div>
        </div>"""

    html += """
    </div>

    <script>
        const cards = document.querySelectorAll('.repo-card');
        const search = document.getElementById('search');
        const filterBtns = document.querySelectorAll('.filter-btn');

        // Search
        search.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            cards.forEach(card => {
                const searchText = card.getAttribute('data-search');
                card.style.display = searchText.includes(term) ? 'block' : 'none';
            });
        });

        // Filters
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.getAttribute('data-filter');
                cards.forEach(card => {
                    const cat = card.getAttribute('data-category');
                    card.style.display = (filter === 'all' || cat === filter) ? 'block' : 'none';
                });
            });
        });
    </script>
</body>
</html>"""

    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Compact overview: {output_path}")
    return output_path


if __name__ == '__main__':
    repos = load_repos()
    create_compact_overview(repos)

    # Also update the main overview
    print("\nUpdating main repository_overview.html to compact version...")
    create_compact_overview(repos, 'docs/visualizations/repository_overview.html')
    print("Done!")
