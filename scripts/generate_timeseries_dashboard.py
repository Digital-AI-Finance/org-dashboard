"""Generate time-series analytics visualizations.

Creates Plotly time-series charts showing repository metrics over time,
including commit frequency, contributor growth, stars/forks, and issue trends.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.research_platform.models.repository import Repository


def load_repositories(repos_file: Path = Path("data/repos.json")) -> list[Repository]:
    """Load repository data from JSON file."""
    if not repos_file.exists():
        raise FileNotFoundError(f"Repository data not found: {repos_file}")

    with open(repos_file, encoding="utf-8") as f:
        repos_data = json.load(f)

    return [Repository.from_dict(repo_data) for repo_data in repos_data]


def fetch_historical_metrics(repositories: list[Repository]) -> dict:
    """
    Fetch historical metrics using PyGithub API.

    Args:
        repositories: List of Repository models

    Returns:
        Dictionary with time-series data
    """
    try:
        from github import Github

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("Warning: GITHUB_TOKEN not set, using mock data")
            return generate_mock_data(repositories)

        g = Github(token)
        metrics = {
            "commits": defaultdict(lambda: defaultdict(int)),  # date -> repo -> count
            "contributors": defaultdict(set),  # date -> set of contributors
            "stars": defaultdict(lambda: defaultdict(int)),  # date -> repo -> cumulative
            "forks": defaultdict(lambda: defaultdict(int)),
            "issues": defaultdict(lambda: defaultdict(int)),
        }

        print("Fetching historical data from GitHub...")

        for repo in repositories:
            try:
                gh_repo = g.get_repo(repo.full_name)
                print(f"  Processing {repo.name}...")

                # Fetch commits (last 90 days)
                since = datetime.now() - timedelta(days=90)
                commits = gh_repo.get_commits(since=since)

                for commit in commits[:100]:  # Limit to avoid rate limits
                    date = commit.commit.author.date.date()
                    date_str = date.isoformat()
                    metrics["commits"][date_str][repo.name] += 1

                    # Track contributors
                    if commit.author:
                        metrics["contributors"][date_str].add(commit.author.login)

                # Current stars and forks (snapshot)
                today = datetime.now().date().isoformat()
                metrics["stars"][today][repo.name] = repo.stars
                metrics["forks"][today][repo.name] = repo.forks

                # Open issues (current)
                metrics["issues"][today][repo.name] = repo.open_issues

            except Exception as e:
                print(f"  Warning: Could not fetch data for {repo.name}: {e}")
                continue

        # Convert sets to counts for contributors
        metrics["contributors"] = {
            date: len(contributors) for date, contributors in metrics["contributors"].items()
        }

        return metrics

    except ImportError:
        print("Warning: PyGithub not installed, using mock data")
        return generate_mock_data(repositories)
    except Exception as e:
        print(f"Warning: Error fetching historical data: {e}")
        return generate_mock_data(repositories)


def generate_mock_data(repositories: list[Repository]) -> dict:
    """Generate mock time-series data for testing."""
    metrics = {
        "commits": defaultdict(lambda: defaultdict(int)),
        "contributors": {},
        "stars": defaultdict(lambda: defaultdict(int)),
        "forks": defaultdict(lambda: defaultdict(int)),
        "issues": defaultdict(lambda: defaultdict(int)),
    }

    # Generate 90 days of mock data
    for i in range(90):
        date = (datetime.now() - timedelta(days=90 - i)).date().isoformat()

        for repo in repositories:
            # Random commits (more recent = more commits)
            import random

            metrics["commits"][date][repo.name] = random.randint(0, max(1, (90 - i) // 10))

        # Contributors (gradually increasing)
        metrics["contributors"][date] = min(len(repositories) + (i // 10), len(repositories) * 2)

    # Current snapshots
    today = datetime.now().date().isoformat()
    for repo in repositories:
        metrics["stars"][today][repo.name] = repo.stars
        metrics["forks"][today][repo.name] = repo.forks
        metrics["issues"][today][repo.name] = repo.open_issues

    return metrics


def create_commit_frequency_chart(metrics: dict, output_path: Path) -> None:
    """Create commit frequency time-series chart."""
    commits = metrics["commits"]

    if not commits:
        print("No commit data available")
        return

    # Aggregate by date
    dates = sorted(commits.keys())
    daily_totals = [sum(commits[date].values()) for date in dates]

    # Calculate 7-day moving average
    moving_avg = []
    window = 7
    for i in range(len(daily_totals)):
        start = max(0, i - window + 1)
        window_data = daily_totals[start : i + 1]
        moving_avg.append(sum(window_data) / len(window_data))

    fig = go.Figure()

    # Daily commits (bar)
    fig.add_trace(
        go.Bar(x=dates, y=daily_totals, name="Daily Commits", marker_color="#003366", opacity=0.6)
    )

    # Moving average (line)
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=moving_avg,
            name="7-Day Average",
            line={"color": "#ff6b6b", "width": 3},
            mode="lines",
        )
    )

    fig.update_layout(
        title={
            "text": "Commit Frequency Over Time",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        xaxis_title="Date",
        yaxis_title="Number of Commits",
        hovermode="x unified",
        height=500,
        showlegend=True,
        template="plotly_white",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Commit frequency chart saved to {output_path}")


def create_contributor_growth_chart(metrics: dict, output_path: Path) -> None:
    """Create contributor growth time-series chart."""
    contributors = metrics["contributors"]

    if not contributors:
        print("No contributor data available")
        return

    dates = sorted(contributors.keys())
    counts = [contributors[date] for date in dates]

    # Calculate cumulative unique contributors
    cumulative = []
    total = 0
    for count in counts:
        total = max(total, count)  # Simplified - assumes non-decreasing
        cumulative.append(total)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=cumulative,
            name="Unique Contributors",
            fill="tozeroy",
            line={"color": "#003366", "width": 2},
            mode="lines+markers",
        )
    )

    fig.update_layout(
        title={
            "text": "Contributor Growth",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        xaxis_title="Date",
        yaxis_title="Cumulative Contributors",
        hovermode="x",
        height=500,
        template="plotly_white",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Contributor growth chart saved to {output_path}")


def create_stars_forks_chart(
    metrics: dict, repositories: list[Repository], output_path: Path
) -> None:
    """Create stars and forks accumulation chart."""
    # Use current values from repositories
    repo_names = [r.name for r in repositories]
    stars = [r.stars for r in repositories]
    forks = [r.forks for r in repositories]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Stars by Repository", "Forks by Repository"),
        specs=[[{"type": "bar"}, {"type": "bar"}]],
    )

    fig.add_trace(go.Bar(x=repo_names, y=stars, name="Stars", marker_color="#ffd700"), row=1, col=1)

    fig.add_trace(go.Bar(x=repo_names, y=forks, name="Forks", marker_color="#003366"), row=1, col=2)

    fig.update_xaxes(title_text="Repository", row=1, col=1, tickangle=-45)
    fig.update_xaxes(title_text="Repository", row=1, col=2, tickangle=-45)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)

    fig.update_layout(
        title={
            "text": "Repository Popularity Metrics",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        height=500,
        showlegend=False,
        template="plotly_white",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Stars/Forks chart saved to {output_path}")


def create_issues_trend_chart(
    metrics: dict, repositories: list[Repository], output_path: Path
) -> None:
    """Create open issues trend chart."""
    repo_names = [r.name for r in repositories if r.open_issues > 0]
    issue_counts = [r.open_issues for r in repositories if r.open_issues > 0]

    if not repo_names:
        print("No open issues data available")
        return

    fig = go.Figure(
        data=[
            go.Bar(
                x=repo_names,
                y=issue_counts,
                marker={
                    "color": issue_counts,
                    "colorscale": "Reds",
                    "showscale": True,
                    "colorbar": {"title": "Open Issues"},
                },
            )
        ]
    )

    fig.update_layout(
        title={
            "text": "Open Issues by Repository",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        xaxis={"title": "Repository", "tickangle": -45},
        yaxis_title="Open Issues",
        height=500,
        template="plotly_white",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Issues trend chart saved to {output_path}")


def main():
    """Generate all time-series visualizations."""
    print("=" * 60)
    print("Time-Series Analytics Generator")
    print("=" * 60)

    # Load data
    print("\nLoading repository data...")
    repositories = load_repositories()
    print(f"Loaded {len(repositories)} repositories")

    # Fetch historical metrics
    print("\nFetching historical metrics...")
    metrics = fetch_historical_metrics(repositories)

    # Create visualizations
    print("\nGenerating time-series charts...")

    # Commit frequency
    commit_path = Path("docs/visualizations/timeseries_commits.html")
    create_commit_frequency_chart(metrics, commit_path)

    # Contributor growth
    contributor_path = Path("docs/visualizations/timeseries_contributors.html")
    create_contributor_growth_chart(metrics, contributor_path)

    # Stars and forks
    stars_path = Path("docs/visualizations/timeseries_stars_forks.html")
    create_stars_forks_chart(metrics, repositories, stars_path)

    # Issues trend
    issues_path = Path("docs/visualizations/timeseries_issues.html")
    create_issues_trend_chart(metrics, repositories, issues_path)

    print("\n" + "=" * 60)
    print("Time-series visualizations generated successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  - {commit_path}")
    print(f"  - {contributor_path}")
    print(f"  - {stars_path}")
    print(f"  - {issues_path}")


if __name__ == "__main__":
    main()
