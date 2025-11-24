#!/usr/bin/env python3
"""
Repository health scoring system.
Combines multiple metrics to assess overall repository health and maintenance.
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Any


class RepositoryHealthScorer:
    """Calculate comprehensive health scores for repositories."""

    def __init__(self):
        self.weights = {
            "activity": 0.25,
            "community": 0.20,
            "documentation": 0.20,
            "code_quality": 0.15,
            "popularity": 0.10,
            "maintenance": 0.10,
        }

    def calculate_activity_score(self, repo: dict[str, Any]) -> dict[str, Any]:
        """Score based on recent activity."""
        score = 0
        details = {}

        # Check last push date
        try:
            last_pushed = datetime.fromisoformat(repo.get("pushed_at", "").replace("Z", "+00:00"))
            days_since_push = (datetime.now(last_pushed.tzinfo) - last_pushed).days

            if days_since_push < 30:
                activity_score = 100
            elif days_since_push < 90:
                activity_score = 75
            elif days_since_push < 180:
                activity_score = 50
            elif days_since_push < 365:
                activity_score = 25
            else:
                activity_score = 10

            score += activity_score
            details["days_since_push"] = days_since_push
            details["activity_score"] = activity_score

        except (ValueError, AttributeError):
            score += 50  # Default for missing data
            details["days_since_push"] = None

        # Check if repo is archived
        if repo.get("archived", False):
            score = max(10, score * 0.1)
            details["archived"] = True
        else:
            details["archived"] = False

        return {"score": min(100, score), "details": details}

    def calculate_community_score(self, repo: dict[str, Any]) -> dict[str, Any]:
        """Score based on community engagement."""
        score = 0
        details = {}

        # Contributors
        contributors = repo.get("contributors_count", 0)
        if contributors >= 10:
            contributor_score = 100
        elif contributors >= 5:
            contributor_score = 75
        elif contributors >= 3:
            contributor_score = 50
        elif contributors >= 2:
            contributor_score = 25
        else:
            contributor_score = 10

        score += contributor_score * 0.5
        details["contributors"] = contributors
        details["contributor_score"] = contributor_score

        # Issues and PRs (if available)
        open_issues = repo.get("open_issues", 0)
        if open_issues > 0:
            score += 25  # Active issues indicate community engagement
            details["has_issues"] = True
        else:
            details["has_issues"] = False

        # Stars and forks
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)

        if stars + forks > 0:
            score += 25
            details["has_engagement"] = True
        else:
            details["has_engagement"] = False

        return {"score": min(100, score), "details": details}

    def calculate_documentation_score(self, repo: dict[str, Any]) -> dict[str, Any]:
        """Score based on documentation quality."""
        score = 0
        details = {}

        # README
        if repo.get("description"):
            score += 30
            details["has_readme"] = True
        else:
            details["has_readme"] = False

        # Description
        if repo.get("description") and len(repo.get("description", "")) > 20:
            score += 20
            details["has_good_description"] = True
        else:
            details["has_good_description"] = False

        # Topics/tags
        topics = repo.get("topics", [])
        if len(topics) >= 3:
            score += 25
        elif len(topics) >= 1:
            score += 15
        details["topic_count"] = len(topics)

        # License
        if repo.get("license") != "No License":
            score += 25
            details["has_license"] = True
        else:
            details["has_license"] = False

        return {"score": min(100, score), "details": details}

    def calculate_code_quality_score(
        self, repo: dict[str, Any], quality_report: dict = None
    ) -> dict[str, Any]:
        """Score based on code quality metrics."""
        if quality_report and repo["name"] in quality_report.get("repositories", {}):
            repo_quality = quality_report["repositories"][repo["name"]]
            structure_score = repo_quality.get("structure", {}).get("structure_score", 50)
            return {"score": structure_score, "details": repo_quality.get("structure", {})}

        # Default scoring without quality report
        score = 50  # Baseline

        # Language suggests structure
        if repo.get("language") in ["Python", "JavaScript", "TypeScript", "Java"]:
            score += 20

        return {"score": score, "details": {"estimated": True}}

    def calculate_popularity_score(self, repo: dict[str, Any]) -> dict[str, Any]:
        """Score based on popularity metrics."""
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)
        repo.get("watchers", stars)  # Often same as stars

        # Logarithmic scoring for stars
        if stars >= 100:
            star_score = 100
        elif stars >= 50:
            star_score = 80
        elif stars >= 20:
            star_score = 60
        elif stars >= 10:
            star_score = 40
        elif stars >= 5:
            star_score = 20
        elif stars >= 1:
            star_score = 10
        else:
            star_score = 0

        # Fork score
        if forks >= 20:
            fork_score = 100
        elif forks >= 10:
            fork_score = 75
        elif forks >= 5:
            fork_score = 50
        elif forks >= 1:
            fork_score = 25
        else:
            fork_score = 0

        score = star_score * 0.7 + fork_score * 0.3

        return {
            "score": score,
            "details": {
                "stars": stars,
                "forks": forks,
                "star_score": star_score,
                "fork_score": fork_score,
            },
        }

    def calculate_maintenance_score(self, repo: dict[str, Any]) -> dict[str, Any]:
        """Score based on maintenance indicators."""
        score = 0
        details = {}

        # Not archived
        if not repo.get("archived", False):
            score += 50
            details["is_active"] = True
        else:
            details["is_active"] = False

        # Has issues enabled (indicates maintenance)
        if repo.get("has_issues", True):
            score += 25
            details["issues_enabled"] = True
        else:
            details["issues_enabled"] = False

        # Default branch exists
        if repo.get("default_branch"):
            score += 25
            details["has_default_branch"] = True
        else:
            details["has_default_branch"] = False

        return {"score": score, "details": details}

    def calculate_overall_health(
        self, repo: dict[str, Any], quality_report: dict = None
    ) -> dict[str, Any]:
        """Calculate comprehensive health score."""
        scores = {}

        # Calculate individual dimension scores
        scores["activity"] = self.calculate_activity_score(repo)
        scores["community"] = self.calculate_community_score(repo)
        scores["documentation"] = self.calculate_documentation_score(repo)
        scores["code_quality"] = self.calculate_code_quality_score(repo, quality_report)
        scores["popularity"] = self.calculate_popularity_score(repo)
        scores["maintenance"] = self.calculate_maintenance_score(repo)

        # Calculate weighted overall score
        overall_score = sum(
            scores[dimension]["score"] * self.weights[dimension] for dimension in self.weights
        )

        # Determine health grade
        if overall_score >= 80:
            grade = "A"
            status = "Excellent"
        elif overall_score >= 70:
            grade = "B"
            status = "Good"
        elif overall_score >= 60:
            grade = "C"
            status = "Fair"
        elif overall_score >= 50:
            grade = "D"
            status = "Poor"
        else:
            grade = "F"
            status = "Critical"

        return {
            "overall_score": round(overall_score, 2),
            "grade": grade,
            "status": status,
            "dimensions": {k: v["score"] for k, v in scores.items()},
            "details": {k: v["details"] for k, v in scores.items()},
        }


def generate_health_report(repos_data: list[dict], quality_report: dict = None) -> dict[str, Any]:
    """Generate health report for all repositories."""
    print("Generating repository health report...")

    scorer = RepositoryHealthScorer()
    health_report = {
        "generated_at": datetime.now().isoformat(),
        "repositories": {},
        "summary": {
            "total_repos": len(repos_data),
            "health_distribution": defaultdict(int),
            "average_scores": {},
        },
    }

    # Calculate health for each repository
    all_dimension_scores = defaultdict(list)

    for repo in repos_data:
        repo_name = repo["name"]
        print(f"  Calculating health for {repo_name}...")

        health = scorer.calculate_overall_health(repo, quality_report)
        health_report["repositories"][repo_name] = health

        # Track for summary
        health_report["summary"]["health_distribution"][health["grade"]] += 1

        for dimension, score in health["dimensions"].items():
            all_dimension_scores[dimension].append(score)

    # Calculate average scores per dimension
    for dimension, scores in all_dimension_scores.items():
        health_report["summary"]["average_scores"][dimension] = round(
            sum(scores) / len(scores) if scores else 0, 2
        )

    # Overall average
    all_overall_scores = [r["overall_score"] for r in health_report["repositories"].values()]
    health_report["summary"]["average_overall_score"] = round(
        sum(all_overall_scores) / len(all_overall_scores) if all_overall_scores else 0, 2
    )

    # Convert defaultdict to dict for JSON serialization
    health_report["summary"]["health_distribution"] = dict(
        health_report["summary"]["health_distribution"]
    )

    # Save report
    output_path = "data/repository_health_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(health_report, f, indent=2, ensure_ascii=False)

    print(f"Health report saved to {output_path}")
    return health_report


def main():
    """Test repository health scorer."""
    print("Repository Health Scorer")
    print("=" * 60)

    if os.path.exists("data/repos.json"):
        with open("data/repos.json", encoding="utf-8") as f:
            repos_data = json.load(f)

        # Load quality report if available
        quality_report = None
        if os.path.exists("data/code_quality_report.json"):
            with open("data/code_quality_report.json", encoding="utf-8") as f:
                quality_report = json.load(f)

        report = generate_health_report(repos_data, quality_report)

        print("\nSummary:")
        print(f"  Total repositories: {report['summary']['total_repos']}")
        print(f"  Average overall score: {report['summary']['average_overall_score']}/100")
        print(f"  Health distribution: {report['summary']['health_distribution']}")
        print("\nAverage dimension scores:")
        for dimension, score in report["summary"]["average_scores"].items():
            print(f"    {dimension}: {score}/100")

    else:
        print("No repos data found. Run build_research_platform.py first.")


if __name__ == "__main__":
    main()
