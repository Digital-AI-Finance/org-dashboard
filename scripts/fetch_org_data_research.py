#!/usr/bin/env python3
"""
Enhanced fetch_org_data with research metadata extraction.
Extends the original fetcher with academic data integration.
"""

import json
import os
import sys
from collections import Counter
from datetime import datetime
from typing import Any

from fetch_academic_data import AcademicDataFetcher
from github import Github, GithubException

# Import our research parsers
from parse_research_metadata import parse_repository_metadata
from tqdm import tqdm


def get_github_client() -> Github:
    """Initialize GitHub client with authentication."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN environment variable not set")
        print("Please set it with: export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)

    try:
        g = Github(token)
        user = g.get_user()
        print(f"Authenticated as: {user.login}")
        return g
    except GithubException as e:
        print(f"ERROR: Failed to authenticate: {e}")
        sys.exit(1)


def fetch_repo_contents(repo) -> list[dict[str, Any]]:
    """
    Fetch repository contents for metadata extraction.
    Returns list of files and directories.
    """
    try:
        contents = []
        # Get root contents
        root_contents = repo.get_contents("")

        def process_contents(items, path=""):
            for item in items:
                item_data = {
                    "name": item.name,
                    "path": item.path,
                    "type": item.type,
                    "size": item.size if hasattr(item, "size") else 0,
                }
                contents.append(item_data)

                # Recursively get directory contents (limit depth to avoid huge repos)
                if item.type == "dir" and path.count("/") < 2:
                    try:
                        dir_contents = repo.get_contents(item.path)
                        process_contents(dir_contents, item.path)
                    except:
                        pass

        process_contents(root_contents)
        return contents
    except Exception as e:
        print(f"Error fetching repo contents: {e}")
        return []


def fetch_repo_data(repo, include_research=True) -> dict[str, Any]:
    """
    Extract relevant data from a repository object.

    Args:
        repo: GitHub repository object
        include_research: Whether to extract research metadata

    Returns:
        Repository data dictionary
    """
    try:
        # Get README content
        readme_content = ""
        try:
            readme = repo.get_readme()
            readme_content = readme.decoded_content.decode("utf-8")
        except:
            readme_content = "No README available"

        # Get contributors count
        try:
            contributors_count = repo.get_contributors().totalCount
        except:
            contributors_count = 0

        # Get latest release
        latest_release = None
        try:
            releases = repo.get_releases()
            if releases.totalCount > 0:
                latest = releases[0]
                latest_release = {
                    "tag": latest.tag_name,
                    "name": latest.title,
                    "published_at": latest.published_at.isoformat()
                    if latest.published_at
                    else None,
                }
        except:
            pass

        # Build basic data structure
        data = {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description or "",
            "url": repo.html_url,
            "clone_url": repo.clone_url,
            "homepage": repo.homepage or "",
            "language": repo.language or "Unknown",
            "topics": repo.get_topics(),
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "open_issues": repo.open_issues_count,
            "size": repo.size,
            "default_branch": repo.default_branch,
            "created_at": repo.created_at.isoformat() if repo.created_at else None,
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
            "license": repo.license.name if repo.license else "No License",
            "has_issues": repo.has_issues,
            "has_wiki": repo.has_wiki,
            "has_pages": repo.has_pages,
            "has_downloads": repo.has_downloads,
            "archived": repo.archived,
            "disabled": repo.disabled,
            "is_template": repo.is_template,
            "visibility": repo.visibility,
            "contributors_count": contributors_count,
            "readme": readme_content,
            "latest_release": latest_release,
        }

        # Add research metadata if requested
        if include_research and readme_content != "No README available":
            print("  Extracting research metadata...")
            try:
                # Fetch repo contents for deeper analysis
                repo_contents = fetch_repo_contents(repo)

                # Parse research metadata
                research_metadata = parse_repository_metadata(data, repo_contents)
                data["research_metadata"] = research_metadata
            except Exception as e:
                print(f"  Warning: Could not extract research metadata: {e}")
                data["research_metadata"] = None

        return data
    except Exception as e:
        print(f"Error fetching data for {repo.name}: {e}")
        return None


def enrich_with_academic_data(repos_data: list[dict], enable=True) -> list[dict]:
    """
    Enrich repository data with academic database information.

    Args:
        repos_data: List of repository data dictionaries
        enable: Whether to fetch from external APIs

    Returns:
        Enriched repository data
    """
    if not enable:
        return repos_data

    print("\nEnriching with academic database information...")
    fetcher = AcademicDataFetcher()

    for repo in tqdm(repos_data, desc="Academic enrichment"):
        research_meta = repo.get("research_metadata")
        if not research_meta:
            continue

        publications = research_meta.get("publications", [])
        if publications:
            try:
                enriched_pubs = fetcher.enrich_publications(publications)
                research_meta["publications"] = enriched_pubs
            except Exception as e:
                print(f"  Error enriching {repo['name']}: {e}")

    return repos_data


def calculate_statistics(repos_data: list[dict]) -> dict[str, Any]:
    """Calculate organization-wide statistics including research metrics."""
    total_repos = len(repos_data)

    # Basic statistics (from original)
    languages = [r["language"] for r in repos_data if r["language"] != "Unknown"]
    language_counts = Counter(languages)

    all_topics = []
    for repo in repos_data:
        all_topics.extend(repo["topics"])
    topic_counts = Counter(all_topics)

    licenses = [r["license"] for r in repos_data]
    license_counts = Counter(licenses)

    total_stars = sum(r["stars"] for r in repos_data)
    total_forks = sum(r["forks"] for r in repos_data)
    total_contributors = sum(r["contributors_count"] for r in repos_data)

    archived_count = sum(1 for r in repos_data if r["archived"])
    active_count = total_repos - archived_count

    sorted_by_activity = sorted(
        [r for r in repos_data if r["pushed_at"]], key=lambda x: x["pushed_at"], reverse=True
    )
    recent_repos = sorted_by_activity[:10]

    sorted_by_stars = sorted(repos_data, key=lambda x: x["stars"], reverse=True)
    popular_repos = sorted_by_stars[:10]

    no_readme = [r["name"] for r in repos_data if r["readme"] == "No README available"]

    avg_stars = total_stars / total_repos if total_repos > 0 else 0
    avg_forks = total_forks / total_repos if total_repos > 0 else 0

    # Research-specific statistics
    repos_with_papers = sum(
        1
        for r in repos_data
        if r.get("research_metadata") and r["research_metadata"].get("publications")
    )
    repos_with_notebooks = sum(
        1
        for r in repos_data
        if r.get("research_metadata") and r["research_metadata"].get("code", {}).get("notebooks")
    )
    repos_with_datasets = sum(
        1
        for r in repos_data
        if r.get("research_metadata") and r["research_metadata"].get("datasets")
    )

    total_publications = sum(
        len(r.get("research_metadata", {}).get("publications", []))
        for r in repos_data
        if r.get("research_metadata")
    )
    total_notebooks = sum(
        len(r.get("research_metadata", {}).get("code", {}).get("notebooks", []))
        for r in repos_data
        if r.get("research_metadata")
    )

    stats = {
        "generated_at": datetime.now().isoformat(),
        "total_repos": total_repos,
        "active_repos": active_count,
        "archived_repos": archived_count,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_contributors": total_contributors,
        "avg_stars": round(avg_stars, 2),
        "avg_forks": round(avg_forks, 2),
        "languages": dict(language_counts.most_common(20)),
        "topics": dict(topic_counts.most_common(20)),
        "licenses": dict(license_counts),
        "recent_repos": [{"name": r["name"], "pushed_at": r["pushed_at"]} for r in recent_repos],
        "popular_repos": [{"name": r["name"], "stars": r["stars"]} for r in popular_repos],
        "repos_without_readme": no_readme,
        # Research statistics
        "research": {
            "repos_with_papers": repos_with_papers,
            "repos_with_notebooks": repos_with_notebooks,
            "repos_with_datasets": repos_with_datasets,
            "total_publications": total_publications,
            "total_notebooks": total_notebooks,
        },
    }

    return stats


def main():
    """Main execution function."""
    print("=" * 60)
    print("GitHub Organization Data Fetcher (with Research Metadata)")
    print("=" * 60)

    # Get organization name
    org_name = os.environ.get("GITHUB_ORG")
    if not org_name and len(sys.argv) > 1:
        org_name = sys.argv[1]

    if not org_name:
        print("ERROR: Organization name not provided")
        print("Usage: python fetch_org_data_research.py ORG_NAME")
        print("   or: export GITHUB_ORG='org_name'")
        sys.exit(1)

    # Check if academic enrichment should be enabled
    enrich_academic = os.environ.get("ENRICH_ACADEMIC", "true").lower() == "true"

    print(f"\nFetching data for organization: {org_name}")
    print(f"Academic enrichment: {'enabled' if enrich_academic else 'disabled'}")

    # Initialize GitHub client
    g = get_github_client()

    # Get organization
    try:
        org = g.get_organization(org_name)
        print(f"Organization found: {org.name or org.login}")
    except GithubException as e:
        print(f"ERROR: Could not find organization '{org_name}': {e}")
        sys.exit(1)

    # Fetch all repositories
    print("\nFetching repositories...")
    repos = list(org.get_repos())
    print(f"Found {len(repos)} repositories")

    # Fetch data for each repository
    print("\nFetching detailed data for each repository...")
    repos_data = []
    for repo in tqdm(repos, desc="Processing repos"):
        data = fetch_repo_data(repo, include_research=True)
        if data:
            repos_data.append(data)

    print(f"\nSuccessfully fetched data for {len(repos_data)} repositories")

    # Enrich with academic data
    if enrich_academic:
        repos_data = enrich_with_academic_data(repos_data, enable=True)

    # Calculate statistics
    print("\nCalculating statistics...")
    stats = calculate_statistics(repos_data)

    # Save to JSON files
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    repos_file = os.path.join(data_dir, "repos.json")
    stats_file = os.path.join(data_dir, "stats.json")
    research_file = os.path.join(data_dir, "research_metadata.json")

    print(f"\nSaving data to {repos_file}...")
    with open(repos_file, "w", encoding="utf-8") as f:
        json.dump(repos_data, f, indent=2, ensure_ascii=False)

    print(f"Saving statistics to {stats_file}...")
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # Save separate research metadata file
    print(f"Saving research metadata to {research_file}...")
    research_data = {
        repo["name"]: repo.get("research_metadata")
        for repo in repos_data
        if repo.get("research_metadata")
    }
    with open(research_file, "w", encoding="utf-8") as f:
        json.dump(research_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("Data fetch completed successfully!")
    print("=" * 60)
    print("\nSummary:")
    print(f"  - Total repositories: {stats['total_repos']}")
    print(f"  - Active repositories: {stats['active_repos']}")
    print(f"  - Total stars: {stats['total_stars']}")
    print(f"  - Total forks: {stats['total_forks']}")
    print(f"  - Repos with publications: {stats['research']['repos_with_papers']}")
    print(f"  - Repos with notebooks: {stats['research']['repos_with_notebooks']}")
    print(f"  - Total publications: {stats['research']['total_publications']}")
    print("\nData saved to:")
    print(f"  - {repos_file}")
    print(f"  - {stats_file}")
    print(f"  - {research_file}")


if __name__ == "__main__":
    main()
