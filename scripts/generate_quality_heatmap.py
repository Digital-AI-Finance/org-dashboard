"""Generate interactive code quality heatmap with real Git data.

Creates a Plotly heatmap showing repository health scores across multiple
quality dimensions, using actual Git commit history and repository metrics.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import plotly.graph_objects as go

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


def fetch_git_metrics(repositories: list[Repository]) -> dict[str, dict]:
    """
    Fetch real Git metrics using PyGithub API.

    Args:
        repositories: List of Repository models

    Returns:
        Dictionary mapping repo names to Git metrics
    """
    try:
        from github import Github

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("Warning: GITHUB_TOKEN not set, skipping Git data fetch")
            return {}

        g = Github(token)
        git_metrics = {}

        for repo in repositories:
            try:
                gh_repo = g.get_repo(repo.full_name)

                # Get commit activity (last 90 days)
                since = datetime.now() - timedelta(days=90)
                commits = gh_repo.get_commits(since=since)
                commit_count_90d = commits.totalCount

                # Get recent commit for freshness
                try:
                    latest_commit = gh_repo.get_commits()[0]
                    days_since_commit = (
                        datetime.now() - latest_commit.commit.author.date.replace(tzinfo=None)
                    ).days
                except Exception:
                    days_since_commit = 999

                # Get issue metrics
                open_issues = gh_repo.open_issues_count

                # Get PR metrics (last 30 days)
                since_pr = datetime.now() - timedelta(days=30)
                prs = gh_repo.get_pulls(state="all", sort="created", direction="desc")
                pr_count_30d = len(
                    [pr for pr in prs if pr.created_at.replace(tzinfo=None) >= since_pr]
                )

                git_metrics[repo.name] = {
                    "commit_count_90d": commit_count_90d,
                    "days_since_commit": days_since_commit,
                    "open_issues": open_issues,
                    "pr_count_30d": pr_count_30d,
                }

                print(f"  Fetched Git data for {repo.name}: {commit_count_90d} commits (90d)")

            except Exception as e:
                print(f"  Warning: Could not fetch Git data for {repo.name}: {e}")
                git_metrics[repo.name] = {
                    "commit_count_90d": 0,
                    "days_since_commit": 999,
                    "open_issues": 0,
                    "pr_count_30d": 0,
                }

        return git_metrics

    except ImportError:
        print("Warning: PyGithub not installed, skipping Git data fetch")
        return {}
    except Exception as e:
        print(f"Warning: Error fetching Git data: {e}")
        return {}


def calculate_quality_matrix(repositories: list[Repository], git_metrics: dict) -> dict:
    """
    Calculate quality scores for heatmap matrix.

    Args:
        repositories: List of Repository models
        git_metrics: Git metrics from fetch_git_metrics()

    Returns:
        Dictionary with matrix data and metadata
    """
    matrix_data = []

    for repo in repositories:
        # Get base health scores from Repository model
        health = repo.calculate_health_score()
        scores = health["scores"]

        # Enhance with real Git data if available
        git_data = git_metrics.get(repo.name, {})

        # Recalculate activity score with real commit data
        activity_score = scores["activity"]
        if git_data.get("commit_count_90d", 0) > 0:
            commits_90d = git_data["commit_count_90d"]
            days_since = git_data["days_since_commit"]

            # Score based on commit frequency and recency
            if days_since < 7:
                activity_score = 25.0
            elif days_since < 30:
                activity_score = 20.0
            elif days_since < 90:
                activity_score = 15.0
            else:
                activity_score = 5.0

            # Boost for high commit volume
            if commits_90d > 50:
                activity_score = min(activity_score + 5, 25.0)
            elif commits_90d > 20:
                activity_score = min(activity_score + 3, 25.0)

        # Calculate collaboration score (based on PRs and contributors)
        collaboration_score = 0.0
        pr_count = git_data.get("pr_count_30d", 0)
        if pr_count > 10:
            collaboration_score = 25.0
        elif pr_count > 5:
            collaboration_score = 20.0
        elif pr_count > 0:
            collaboration_score = 15.0

        # Adjust for contributor count
        if repo.contributors_count > 5:
            collaboration_score = min(collaboration_score + 10, 25.0)
        elif repo.contributors_count > 2:
            collaboration_score = min(collaboration_score + 5, 25.0)

        # Use existing scores for community and documentation
        community_score = scores["community"]
        documentation_score = scores["documentation"]
        code_quality_score = scores["code_quality"]

        # Overall score
        overall = (
            activity_score
            + community_score
            + documentation_score
            + code_quality_score
            + collaboration_score
        )
        overall = min(overall, 100.0)  # Cap at 100

        row = {
            "repository": repo.name,
            "full_name": repo.full_name,
            "activity": activity_score,
            "community": community_score,
            "documentation": documentation_score,
            "code_quality": code_quality_score,
            "collaboration": collaboration_score,
            "overall": overall,
            "grade": Repository._score_to_grade(overall),
            "stars": repo.stars,
            "language": repo.language or "Unknown",
        }

        matrix_data.append(row)

    # Sort by overall score (descending)
    matrix_data.sort(key=lambda x: x["overall"], reverse=True)

    return {
        "matrix": matrix_data,
        "dimensions": [
            "Activity",
            "Community",
            "Documentation",
            "Code Quality",
            "Collaboration",
            "Overall",
        ],
        "total_repositories": len(repositories),
    }


def create_quality_heatmap(matrix_data: dict, output_path: Path) -> None:
    """
    Create interactive quality heatmap visualization.

    Args:
        matrix_data: Matrix data from calculate_quality_matrix()
        output_path: Path to save HTML file
    """
    matrix = matrix_data["matrix"]
    dimensions = matrix_data["dimensions"]

    if not matrix:
        print("Warning: No repository data available for heatmap")
        return

    # Prepare data for heatmap
    repo_names = [row["repository"] for row in matrix]

    # Build z-matrix (rows=repos, cols=dimensions)
    z_data = []
    hover_texts = []

    for row in matrix:
        z_row = [
            row["activity"],
            row["community"],
            row["documentation"],
            row["code_quality"],
            row["collaboration"],
            row["overall"],
        ]
        z_data.append(z_row)

        # Build hover text for each cell
        hover_row = []
        for dim, score in zip(dimensions, z_row):
            grade = Repository._score_to_grade(score)
            hover_row.append(
                f"<b>{row['repository']}</b><br>"
                f"{dim}: {score:.1f}/25.0<br>"
                f"Grade: {grade}<br>"
                f"Language: {row['language']}<br>"
                f"Stars: {row['stars']}"
            )
        hover_texts.append(hover_row)

    # Define colorscale (green=high, red=low)
    colorscale = [
        [0.0, "#d32f2f"],  # Red (F)
        [0.6, "#ff9800"],  # Orange (D)
        [0.7, "#fdd835"],  # Yellow (C)
        [0.8, "#7cb342"],  # Light green (B)
        [1.0, "#2e7d32"],  # Dark green (A)
    ]

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=z_data,
            x=dimensions,
            y=repo_names,
            colorscale=colorscale,
            hovertext=hover_texts,
            hovertemplate="%{hovertext}<extra></extra>",
            colorbar={
                "title": "Score",
                "tickvals": [0, 15, 17.5, 20, 22.5, 25],
                "ticktext": ["F (0)", "D (15)", "C (17.5)", "B (20)", "A (22.5)", "25"],
            },
        )
    )

    # Update layout
    fig.update_layout(
        title={
            "text": f"Repository Quality Heatmap - {matrix_data['total_repositories']} Repositories",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        xaxis={
            "title": "Quality Dimensions",
            "side": "bottom",
        },
        yaxis={
            "title": "Repositories",
            "autorange": "reversed",  # Top to bottom (best to worst)
        },
        height=max(600, len(repo_names) * 30),  # Dynamic height based on repo count
        margin={"l": 200, "r": 100, "t": 80, "b": 80},
        font={"family": "Arial, sans-serif", "size": 12},
    )

    # Save HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path))
    print(f"Quality heatmap saved to {output_path}")


def main():
    """Generate code quality heatmap with real Git data."""
    print("=" * 60)
    print("Code Quality Heatmap Generator")
    print("=" * 60)

    # Load data
    print("\nLoading repository data...")
    repositories = load_repositories()
    print(f"Loaded {len(repositories)} repositories")

    # Fetch Git metrics
    print("\nFetching Git metrics (this may take a minute)...")
    git_metrics = fetch_git_metrics(repositories)
    print(f"Fetched Git data for {len(git_metrics)} repositories")

    # Calculate quality matrix
    print("\nCalculating quality scores...")
    matrix_data = calculate_quality_matrix(repositories, git_metrics)

    # Print summary
    print("\nQuality Score Summary:")
    for row in matrix_data["matrix"][:5]:
        print(f"  {row['repository']:<30} | Grade: {row['grade']} | Overall: {row['overall']:.1f}")

    # Create visualization
    print("\nGenerating heatmap visualization...")
    output_path = Path("docs/visualizations/code_quality_heatmap.html")
    create_quality_heatmap(matrix_data, output_path)

    print("\n" + "=" * 60)
    print("Code quality heatmap generated successfully!")
    print("=" * 60)
    print(f"\nGenerated file: {output_path}")


if __name__ == "__main__":
    main()
