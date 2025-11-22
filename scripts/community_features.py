#!/usr/bin/env python3
"""
Community features: replication tracking, verification system, reproducibility scores.
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Any


class ReplicationTracker:
    """Track replication attempts and results."""

    def __init__(self, data_file="data/replications.json"):
        self.data_file = data_file
        self.replications = self.load_replications()

    def load_replications(self) -> dict:
        """Load replication data from file."""
        if os.path.exists(self.data_file):
            with open(self.data_file) as f:
                return json.load(f)
        return {}

    def save_replications(self) -> None:
        """Save replication data to file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump(self.replications, f, indent=2)

    def add_replication_attempt(
        self, repo_name: str, user: str, status: str, notes: str = "", environment: dict = None
    ) -> str:
        """
        Record a replication attempt.

        Args:
            repo_name: Repository name
            user: Username attempting replication
            status: 'success', 'partial', 'failed'
            notes: Additional notes
            environment: Dict with environment info (OS, Python version, etc.)

        Returns:
            Replication ID
        """
        if repo_name not in self.replications:
            self.replications[repo_name] = []

        replication_id = f"rep_{len(self.replications[repo_name])}"

        attempt = {
            "id": replication_id,
            "user": user,
            "status": status,
            "notes": notes,
            "timestamp": datetime.now().isoformat(),
            "environment": environment or {},
        }

        self.replications[repo_name].append(attempt)
        self.save_replications()

        return replication_id

    def get_replication_stats(self, repo_name: str) -> dict:
        """Get replication statistics for a repository."""
        if repo_name not in self.replications:
            return {
                "total_attempts": 0,
                "success_count": 0,
                "partial_count": 0,
                "failed_count": 0,
                "success_rate": 0.0,
            }

        attempts = self.replications[repo_name]
        total = len(attempts)
        success = sum(1 for a in attempts if a["status"] == "success")
        partial = sum(1 for a in attempts if a["status"] == "partial")
        failed = sum(1 for a in attempts if a["status"] == "failed")

        return {
            "total_attempts": total,
            "success_count": success,
            "partial_count": partial,
            "failed_count": failed,
            "success_rate": success / total if total > 0 else 0.0,
            "latest_attempt": attempts[-1] if attempts else None,
        }


class VerificationSystem:
    """Community verification and peer review system."""

    def __init__(self, data_file="data/verifications.json"):
        self.data_file = data_file
        self.verifications = self.load_verifications()

    def load_verifications(self) -> dict:
        """Load verification data."""
        if os.path.exists(self.data_file):
            with open(self.data_file) as f:
                return json.load(f)
        return {}

    def save_verifications(self) -> None:
        """Save verification data."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump(self.verifications, f, indent=2)

    def add_verification(
        self, repo_name: str, reviewer: str, category: str, rating: int, comments: str = ""
    ) -> str:
        """
        Add a verification review.

        Args:
            repo_name: Repository name
            reviewer: Reviewer username
            category: Verification category (code_quality, documentation, reproducibility, etc.)
            rating: Rating 1-5
            comments: Review comments

        Returns:
            Verification ID
        """
        if repo_name not in self.verifications:
            self.verifications[repo_name] = []

        verification_id = f"ver_{len(self.verifications[repo_name])}"

        verification = {
            "id": verification_id,
            "reviewer": reviewer,
            "category": category,
            "rating": rating,
            "comments": comments,
            "timestamp": datetime.now().isoformat(),
        }

        self.verifications[repo_name].append(verification)
        self.save_verifications()

        return verification_id

    def get_verification_summary(self, repo_name: str) -> dict:
        """Get verification summary for a repository."""
        if repo_name not in self.verifications:
            return {"total_reviews": 0, "average_rating": 0.0, "category_ratings": {}}

        verifications = self.verifications[repo_name]

        # Calculate averages by category
        category_ratings = defaultdict(list)
        for v in verifications:
            category_ratings[v["category"]].append(v["rating"])

        category_averages = {
            cat: sum(ratings) / len(ratings) for cat, ratings in category_ratings.items()
        }

        all_ratings = [v["rating"] for v in verifications]
        avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0.0

        return {
            "total_reviews": len(verifications),
            "average_rating": round(avg_rating, 2),
            "category_ratings": category_averages,
        }


class ReproducibilityScorer:
    """Calculate reproducibility scores for repositories."""

    def calculate_score(self, repo_data: dict) -> dict[str, Any]:
        """
        Calculate reproducibility score based on multiple factors.

        Returns:
            Dictionary with score and breakdown
        """
        score = 0
        max_score = 100
        breakdown = {}

        research_meta = repo_data.get("research_metadata", {})
        reproducibility = research_meta.get("reproducibility", {})

        # Documentation (30 points)
        doc_score = 0
        if repo_data.get("readme") and repo_data["readme"] != "No README available":
            doc_score += 10
        if research_meta.get("research", {}).get("abstract"):
            doc_score += 10
        if research_meta.get("publications"):
            doc_score += 10
        breakdown["documentation"] = doc_score

        # Environment specification (25 points)
        env_score = 0
        if reproducibility.get("has_requirements"):
            env_score += 10
        if reproducibility.get("has_dockerfile"):
            env_score += 10
        if reproducibility.get("has_environment_yml"):
            env_score += 5
        breakdown["environment"] = env_score

        # Data availability (20 points)
        data_score = 0
        datasets = research_meta.get("datasets", [])
        if len(datasets) > 0:
            data_score += 10
        if len(datasets) > 3:
            data_score += 10
        breakdown["data"] = data_score

        # Code quality (15 points)
        code_score = 0
        if research_meta.get("code", {}).get("notebooks"):
            code_score += 10
        if repo_data.get("has_wiki"):
            code_score += 5
        breakdown["code"] = code_score

        # Community verification (10 points)
        verifier = VerificationSystem()
        verification = verifier.get_verification_summary(repo_data["name"])
        if verification["total_reviews"] > 0:
            community_score = min(10, verification["average_rating"] * 2)
        else:
            community_score = 0
        breakdown["community"] = community_score

        # Total score
        score = sum(breakdown.values())

        # Get badge level
        if score >= 80:
            badge = "gold"
        elif score >= 60:
            badge = "silver"
        elif score >= 40:
            badge = "bronze"
        else:
            badge = "none"

        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 1),
            "badge": badge,
            "breakdown": breakdown,
        }


def generate_reproducibility_report(repos_data: list[dict]) -> dict:
    """Generate comprehensive reproducibility report for all repos."""
    print("Generating reproducibility report...")

    scorer = ReproducibilityScorer()
    tracker = ReplicationTracker()
    verifier = VerificationSystem()

    report = {"generated_at": datetime.now().isoformat(), "repositories": {}}

    for repo in repos_data:
        repo_name = repo["name"]

        # Calculate reproducibility score
        score_data = scorer.calculate_score(repo)

        # Get replication stats
        replication_stats = tracker.get_replication_stats(repo_name)

        # Get verification summary
        verification = verifier.get_verification_summary(repo_name)

        report["repositories"][repo_name] = {
            "reproducibility_score": score_data,
            "replication_stats": replication_stats,
            "community_verification": verification,
        }

    # Calculate organization-level stats
    all_scores = [r["reproducibility_score"]["score"] for r in report["repositories"].values()]
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    badge_counts = defaultdict(int)
    for r in report["repositories"].values():
        badge_counts[r["reproducibility_score"]["badge"]] += 1

    report["organization_summary"] = {
        "average_reproducibility_score": round(avg_score, 2),
        "total_repositories": len(repos_data),
        "badge_distribution": dict(badge_counts),
        "top_repos": sorted(
            report["repositories"].items(),
            key=lambda x: x[1]["reproducibility_score"]["score"],
            reverse=True,
        )[:10],
    }

    # Save report
    os.makedirs("data", exist_ok=True)
    with open("data/reproducibility_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Reproducibility report saved to data/reproducibility_report.json")
    return report


def main():
    """Test community features."""
    print("Community Features System")
    print("=" * 60)

    # Test replication tracker
    print("\n1. Testing Replication Tracker...")
    tracker = ReplicationTracker()

    # Add sample replication
    rep_id = tracker.add_replication_attempt(
        repo_name="test-repo",
        user="test-user",
        status="success",
        notes="Successfully replicated on Ubuntu 22.04",
        environment={"os": "Ubuntu 22.04", "python": "3.11"},
    )
    print(f"   Added replication: {rep_id}")

    stats = tracker.get_replication_stats("test-repo")
    print(f"   Replication stats: {stats}")

    # Test verification system
    print("\n2. Testing Verification System...")
    verifier = VerificationSystem()

    ver_id = verifier.add_verification(
        repo_name="test-repo",
        reviewer="reviewer1",
        category="code_quality",
        rating=4,
        comments="Well documented code",
    )
    print(f"   Added verification: {ver_id}")

    summary = verifier.get_verification_summary("test-repo")
    print(f"   Verification summary: {summary}")

    # Load and test with real data if available
    if os.path.exists("data/repos.json"):
        print("\n3. Generating Reproducibility Report...")
        with open("data/repos.json") as f:
            repos_data = json.load(f)

        report = generate_reproducibility_report(repos_data)
        print(
            f"   Average org score: {report['organization_summary']['average_reproducibility_score']}"
        )
        print(f"   Badge distribution: {report['organization_summary']['badge_distribution']}")


if __name__ == "__main__":
    main()
