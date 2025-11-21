#!/usr/bin/env python3
"""
Fetch organization data from GitHub API and save to JSON files.
"""

import json
import os
import sys
from datetime import datetime
from collections import Counter
from typing import Dict, List, Any

from github import Github, GithubException
from tqdm import tqdm


def get_github_client() -> Github:
    """Initialize GitHub client with authentication."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("ERROR: GITHUB_TOKEN environment variable not set")
        print("Please set it with: export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)

    try:
        g = Github(token)
        # Test authentication
        user = g.get_user()
        print(f"Authenticated as: {user.login}")
        return g
    except GithubException as e:
        print(f"ERROR: Failed to authenticate: {e}")
        sys.exit(1)


def fetch_repo_data(repo) -> Dict[str, Any]:
    """Extract relevant data from a repository object."""
    try:
        # Get README content
        readme_content = ""
        try:
            readme = repo.get_readme()
            readme_content = readme.decoded_content.decode('utf-8')
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
                    'tag': latest.tag_name,
                    'name': latest.title,
                    'published_at': latest.published_at.isoformat() if latest.published_at else None
                }
        except:
            pass

        # Build data structure
        data = {
            'name': repo.name,
            'full_name': repo.full_name,
            'description': repo.description or "",
            'url': repo.html_url,
            'clone_url': repo.clone_url,
            'homepage': repo.homepage or "",
            'language': repo.language or "Unknown",
            'topics': repo.get_topics(),
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'watchers': repo.watchers_count,
            'open_issues': repo.open_issues_count,
            'size': repo.size,
            'default_branch': repo.default_branch,
            'created_at': repo.created_at.isoformat() if repo.created_at else None,
            'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
            'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None,
            'license': repo.license.name if repo.license else "No License",
            'has_issues': repo.has_issues,
            'has_wiki': repo.has_wiki,
            'has_pages': repo.has_pages,
            'has_downloads': repo.has_downloads,
            'archived': repo.archived,
            'disabled': repo.disabled,
            'is_template': repo.is_template,
            'visibility': repo.visibility,
            'contributors_count': contributors_count,
            'readme': readme_content,
            'latest_release': latest_release
        }

        return data
    except Exception as e:
        print(f"Error fetching data for {repo.name}: {e}")
        return None


def calculate_statistics(repos_data: List[Dict]) -> Dict[str, Any]:
    """Calculate organization-wide statistics."""
    total_repos = len(repos_data)

    # Language distribution
    languages = [r['language'] for r in repos_data if r['language'] != "Unknown"]
    language_counts = Counter(languages)

    # Topic distribution
    all_topics = []
    for repo in repos_data:
        all_topics.extend(repo['topics'])
    topic_counts = Counter(all_topics)

    # License distribution
    licenses = [r['license'] for r in repos_data]
    license_counts = Counter(licenses)

    # Calculate totals
    total_stars = sum(r['stars'] for r in repos_data)
    total_forks = sum(r['forks'] for r in repos_data)
    total_contributors = sum(r['contributors_count'] for r in repos_data)

    # Activity metrics
    archived_count = sum(1 for r in repos_data if r['archived'])
    active_count = total_repos - archived_count

    # Find most active repos (by recent push)
    sorted_by_activity = sorted(
        [r for r in repos_data if r['pushed_at']],
        key=lambda x: x['pushed_at'],
        reverse=True
    )
    recent_repos = sorted_by_activity[:10]

    # Find most popular repos
    sorted_by_stars = sorted(repos_data, key=lambda x: x['stars'], reverse=True)
    popular_repos = sorted_by_stars[:10]

    # Repos without README
    no_readme = [r['name'] for r in repos_data if r['readme'] == "No README available"]

    # Calculate average metrics
    avg_stars = total_stars / total_repos if total_repos > 0 else 0
    avg_forks = total_forks / total_repos if total_repos > 0 else 0

    stats = {
        'generated_at': datetime.now().isoformat(),
        'total_repos': total_repos,
        'active_repos': active_count,
        'archived_repos': archived_count,
        'total_stars': total_stars,
        'total_forks': total_forks,
        'total_contributors': total_contributors,
        'avg_stars': round(avg_stars, 2),
        'avg_forks': round(avg_forks, 2),
        'languages': dict(language_counts.most_common(20)),
        'topics': dict(topic_counts.most_common(20)),
        'licenses': dict(license_counts),
        'recent_repos': [{'name': r['name'], 'pushed_at': r['pushed_at']} for r in recent_repos],
        'popular_repos': [{'name': r['name'], 'stars': r['stars']} for r in popular_repos],
        'repos_without_readme': no_readme
    }

    return stats


def main():
    """Main execution function."""
    print("=" * 60)
    print("GitHub Organization Data Fetcher")
    print("=" * 60)

    # Get organization name from environment or command line
    org_name = os.environ.get('GITHUB_ORG')
    if not org_name and len(sys.argv) > 1:
        org_name = sys.argv[1]

    if not org_name:
        print("ERROR: Organization name not provided")
        print("Usage: python fetch_org_data.py ORG_NAME")
        print("   or: export GITHUB_ORG='org_name'")
        sys.exit(1)

    print(f"\nFetching data for organization: {org_name}")

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
        data = fetch_repo_data(repo)
        if data:
            repos_data.append(data)

    print(f"\nSuccessfully fetched data for {len(repos_data)} repositories")

    # Calculate statistics
    print("\nCalculating statistics...")
    stats = calculate_statistics(repos_data)

    # Save to JSON files
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    repos_file = os.path.join(data_dir, 'repos.json')
    stats_file = os.path.join(data_dir, 'stats.json')

    print(f"\nSaving data to {repos_file}...")
    with open(repos_file, 'w', encoding='utf-8') as f:
        json.dump(repos_data, f, indent=2, ensure_ascii=False)

    print(f"Saving statistics to {stats_file}...")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("Data fetch completed successfully!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total repositories: {stats['total_repos']}")
    print(f"  - Active repositories: {stats['active_repos']}")
    print(f"  - Total stars: {stats['total_stars']}")
    print(f"  - Total forks: {stats['total_forks']}")
    print(f"  - Top language: {list(stats['languages'].keys())[0] if stats['languages'] else 'N/A'}")
    print(f"\nData saved to:")
    print(f"  - {repos_file}")
    print(f"  - {stats_file}")


if __name__ == '__main__':
    main()
