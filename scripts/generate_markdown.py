#!/usr/bin/env python3
"""
Generate markdown files from GitHub organization data.
"""

import json
import os
from collections import defaultdict
from datetime import datetime

from jinja2 import Environment, FileSystemLoader


def load_data():
    """Load repos and stats data from JSON files."""
    with open("data/repos.json", encoding="utf-8") as f:
        repos = json.load(f)

    with open("data/stats.json", encoding="utf-8") as f:
        stats = json.load(f)

    return repos, stats


def format_date(date_str):
    """Format ISO date string to readable format."""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except:
        return date_str


def format_number(num):
    """Format large numbers with commas."""
    return f"{num:,}"


def setup_jinja_env():
    """Set up Jinja2 environment with custom filters."""
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_date"] = format_date
    env.filters["format_number"] = format_number
    return env


def generate_repo_pages(repos, env):
    """Generate individual repository markdown files."""
    print(f"Generating {len(repos)} repository pages...")

    os.makedirs("docs/repos", exist_ok=True)

    template = env.get_template("repo_research.md.j2")

    for repo in repos:
        filename = f"docs/repos/{repo['name']}.md"
        content = template.render(repo=repo)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  Created {len(repos)} repo pages in docs/repos/")


def generate_repos_index(repos, env):
    """Generate main repositories index page."""
    print("Generating repositories index...")

    template = env.get_template("repos_index.md.j2")

    # Sort repos by name
    sorted_repos = sorted(repos, key=lambda x: x["name"].lower())

    content = template.render(repos=sorted_repos, count=len(repos))

    with open("docs/repos/index.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("  Created docs/repos/index.md")


def generate_language_pages(repos, stats, env):
    """Generate language category pages."""
    print("Generating language pages...")

    os.makedirs("docs/by-language", exist_ok=True)

    # Group repos by language
    by_language = defaultdict(list)
    for repo in repos:
        lang = repo["language"] if repo["language"] != "Unknown" else "Unknown"
        by_language[lang].append(repo)

    # Generate overview page
    template_overview = env.get_template("language_overview.md.j2")
    content = template_overview.render(
        languages=stats["languages"], language_count=len(by_language)
    )
    with open("docs/by-language/index.md", "w", encoding="utf-8") as f:
        f.write(content)

    # Generate individual language pages
    template = env.get_template("language.md.j2")
    for language, lang_repos in by_language.items():
        filename = f"docs/by-language/{language.lower().replace(' ', '-').replace('#', 'sharp').replace('+', 'plus')}.md"
        sorted_repos = sorted(lang_repos, key=lambda x: x["stars"], reverse=True)

        content = template.render(language=language, repos=sorted_repos, count=len(sorted_repos))

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  Created {len(by_language)} language pages in docs/by-language/")


def generate_topic_pages(repos, stats, env):
    """Generate topic category pages."""
    print("Generating topic pages...")

    os.makedirs("docs/by-topic", exist_ok=True)

    # Group repos by topic
    by_topic = defaultdict(list)
    for repo in repos:
        for topic in repo["topics"]:
            by_topic[topic].append(repo)

    # Generate overview page
    template_overview = env.get_template("topic_overview.md.j2")
    content = template_overview.render(topics=stats["topics"], topic_count=len(by_topic))
    with open("docs/by-topic/index.md", "w", encoding="utf-8") as f:
        f.write(content)

    # Generate individual topic pages
    template = env.get_template("topic.md.j2")
    for topic, topic_repos in by_topic.items():
        filename = f"docs/by-topic/{topic.lower().replace(' ', '-')}.md"
        sorted_repos = sorted(topic_repos, key=lambda x: x["stars"], reverse=True)

        content = template.render(topic=topic, repos=sorted_repos, count=len(sorted_repos))

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  Created {len(by_topic)} topic pages in docs/by-topic/")


def generate_main_index(repos, stats, env):
    """Generate main index page."""
    print("Generating main index page...")

    template = env.get_template("index.md.j2")
    content = template.render(stats=stats, repo_count=len(repos))

    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("  Created docs/index.md")


def generate_stats_page(stats, env):
    """Generate statistics page."""
    print("Generating statistics page...")

    template = env.get_template("stats.md.j2")
    content = template.render(stats=stats)

    with open("docs/stats.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("  Created docs/stats.md")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Markdown Generator")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    repos, stats = load_data()
    print(f"  Loaded {len(repos)} repositories")

    # Set up Jinja2
    env = setup_jinja_env()

    # Generate all markdown files
    print("\nGenerating markdown files...")
    generate_main_index(repos, stats, env)
    generate_stats_page(stats, env)
    generate_repos_index(repos, env)
    generate_repo_pages(repos, env)
    generate_language_pages(repos, stats, env)
    generate_topic_pages(repos, stats, env)

    print("\n" + "=" * 60)
    print("Markdown generation completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
