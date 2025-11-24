#!/usr/bin/env python3
"""
Seed example community verification data for demonstration purposes.
"""

import json
from datetime import datetime, timedelta


def load_reproducibility_report():
    """Load the existing reproducibility report."""
    with open("data/reproducibility_report.json") as f:
        return json.load(f)


def seed_replication_attempts(report):
    """Add example replication attempts to repositories."""
    # Define example replications
    replications = [
        {
            "repo": "portfolio-optimization-ml",
            "attempts": [
                {
                    "user": "researcher123",
                    "date": (datetime.now() - timedelta(days=15)).isoformat(),
                    "status": "success",
                    "environment": "Python 3.9, Ubuntu 22.04",
                    "duration_hours": 4.5,
                    "notes": "Successfully replicated all main results. DQN model achieved similar performance to reported metrics.",
                },
                {
                    "user": "phd_student_ai",
                    "date": (datetime.now() - timedelta(days=30)).isoformat(),
                    "status": "partial",
                    "environment": "Python 3.10, macOS",
                    "duration_hours": 6.0,
                    "notes": "Replicated training procedure but had issues with GPU acceleration on M1 Mac. Results within 5% of reported.",
                },
                {
                    "user": "quant_trader",
                    "date": (datetime.now() - timedelta(days=45)).isoformat(),
                    "status": "success",
                    "environment": "Python 3.9, Windows 11",
                    "duration_hours": 5.5,
                    "notes": "All experiments reproduced successfully. Very well documented code!",
                },
            ],
        },
        {
            "repo": "credit-risk-prediction",
            "attempts": [
                {
                    "user": "ml_researcher",
                    "date": (datetime.now() - timedelta(days=10)).isoformat(),
                    "status": "success",
                    "environment": "Python 3.9, Ubuntu 20.04, CUDA 11.2",
                    "duration_hours": 3.0,
                    "notes": "Clean code and excellent documentation. SHAP values matched published figures.",
                },
                {
                    "user": "data_scientist_99",
                    "date": (datetime.now() - timedelta(days=25)).isoformat(),
                    "status": "failed",
                    "environment": "Python 3.11, Ubuntu 22.04",
                    "duration_hours": 2.0,
                    "notes": "Missing dependency versions caused issues. TensorFlow 2.13+ broke compatibility.",
                },
            ],
        },
        {
            "repo": "market-microstructure",
            "attempts": [
                {
                    "user": "trading_researcher",
                    "date": (datetime.now() - timedelta(days=5)).isoformat(),
                    "status": "partial",
                    "environment": "Python 3.9, Docker container",
                    "duration_hours": 8.0,
                    "notes": "Docker setup worked perfectly. Data preprocessing successful but full analysis requires proprietary exchange data.",
                }
            ],
        },
    ]

    # Add replication attempts to report
    for replication in replications:
        repo_name = replication["repo"]
        if repo_name in report["repositories"]:
            repo_data = report["repositories"][repo_name]

            # Calculate stats
            total = len(replication["attempts"])
            success = sum(1 for a in replication["attempts"] if a["status"] == "success")
            partial = sum(1 for a in replication["attempts"] if a["status"] == "partial")
            failed = sum(1 for a in replication["attempts"] if a["status"] == "failed")

            repo_data["replication_stats"] = {
                "total_attempts": total,
                "success_count": success,
                "partial_count": partial,
                "failed_count": failed,
                "success_rate": (success / total * 100) if total > 0 else 0.0,
                "attempts": replication["attempts"],
            }

    return report


def seed_community_reviews(report):
    """Add example community verification reviews."""
    reviews = [
        {
            "repo": "portfolio-optimization-ml",
            "reviews": [
                {
                    "reviewer": "prof_finance",
                    "date": (datetime.now() - timedelta(days=20)).isoformat(),
                    "overall_rating": 9,
                    "category_ratings": {
                        "code_quality": 9,
                        "documentation": 10,
                        "reproducibility": 8,
                        "data_availability": 7,
                    },
                    "comment": "Excellent research software. Minor issues with data availability but overall outstanding.",
                },
                {
                    "reviewer": "quant_researcher",
                    "date": (datetime.now() - timedelta(days=35)).isoformat(),
                    "overall_rating": 8,
                    "category_ratings": {
                        "code_quality": 8,
                        "documentation": 9,
                        "reproducibility": 8,
                        "data_availability": 6,
                    },
                    "comment": "Well-structured code. Would benefit from more detailed hyperparameter documentation.",
                },
            ],
        },
        {
            "repo": "credit-risk-prediction",
            "reviews": [
                {
                    "reviewer": "ml_expert",
                    "date": (datetime.now() - timedelta(days=12)).isoformat(),
                    "overall_rating": 9,
                    "category_ratings": {
                        "code_quality": 10,
                        "documentation": 9,
                        "reproducibility": 9,
                        "data_availability": 8,
                    },
                    "comment": "Exceptional work on explainability. Notebooks are very well-crafted.",
                }
            ],
        },
        {
            "repo": "market-microstructure",
            "reviews": [
                {
                    "reviewer": "hft_specialist",
                    "date": (datetime.now() - timedelta(days=8)).isoformat(),
                    "overall_rating": 7,
                    "category_ratings": {
                        "code_quality": 9,
                        "documentation": 8,
                        "reproducibility": 6,
                        "data_availability": 5,
                    },
                    "comment": "Code quality is excellent but reproducibility limited by data availability. Docker setup is great.",
                }
            ],
        },
    ]

    # Add reviews to report
    for review_set in reviews:
        repo_name = review_set["repo"]
        if repo_name in report["repositories"]:
            repo_data = report["repositories"][repo_name]

            # Calculate average ratings
            total_reviews = len(review_set["reviews"])
            avg_overall = sum(r["overall_rating"] for r in review_set["reviews"]) / total_reviews

            # Calculate category averages
            categories = {}
            for category in [
                "code_quality",
                "documentation",
                "reproducibility",
                "data_availability",
            ]:
                ratings = [r["category_ratings"][category] for r in review_set["reviews"]]
                categories[category] = sum(ratings) / len(ratings)

            repo_data["community_verification"] = {
                "total_reviews": total_reviews,
                "average_rating": round(avg_overall, 1),
                "category_ratings": {k: round(v, 1) for k, v in categories.items()},
                "reviews": review_set["reviews"],
            }

    return report


def update_reproducibility_scores(report):
    """Update reproducibility scores based on community data."""
    for _repo_name, repo_data in report["repositories"].items():
        score_data = repo_data["reproducibility_score"]

        # Boost community score if there are successful replications
        if repo_data["replication_stats"]["total_attempts"] > 0:
            success_rate = repo_data["replication_stats"]["success_rate"]
            # Award up to 20 points for community replications
            community_points = min(20, int(success_rate / 5))
            score_data["breakdown"]["community"] = community_points

            # Recalculate total score
            score_data["score"] = sum(score_data["breakdown"].values())
            score_data["percentage"] = (score_data["score"] / score_data["max_score"]) * 100

            # Update badge
            if score_data["percentage"] >= 80:
                score_data["badge"] = "gold"
            elif score_data["percentage"] >= 60:
                score_data["badge"] = "silver"
            elif score_data["percentage"] >= 40:
                score_data["badge"] = "bronze"
            else:
                score_data["badge"] = "none"

    return report


def main():
    """Seed all community data."""
    print("=" * 60)
    print("Seeding Community Verification Data")
    print("=" * 60)

    print("\nLoading reproducibility report...")
    report = load_reproducibility_report()
    print(f"  Found {len(report['repositories'])} repositories")

    print("\nAdding replication attempts...")
    report = seed_replication_attempts(report)
    total_attempts = sum(
        r["replication_stats"]["total_attempts"] for r in report["repositories"].values()
    )
    print(f"  Added {total_attempts} replication attempts")

    print("\nAdding community reviews...")
    report = seed_community_reviews(report)
    total_reviews = sum(
        r["community_verification"]["total_reviews"]
        for r in report["repositories"].values()
        if "community_verification" in r
    )
    print(f"  Added {total_reviews} community reviews")

    print("\nUpdating reproducibility scores...")
    report = update_reproducibility_scores(report)

    print("\nSaving updated report...")
    with open("data/reproducibility_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print("Community Data Seeding Complete!")
    print("=" * 60)

    # Print summary
    print("\nUpdated Reproducibility Scores:")
    for repo_name, repo_data in report["repositories"].items():
        score = repo_data["reproducibility_score"]["score"]
        badge = repo_data["reproducibility_score"]["badge"].upper()
        attempts = repo_data["replication_stats"]["total_attempts"]
        success_rate = repo_data["replication_stats"]["success_rate"]
        print(f"  {repo_name}:")
        print(f"    Score: {score}/100 ({badge})")
        print(f"    Replications: {attempts} attempts, {success_rate:.0f}% success rate")


if __name__ == "__main__":
    main()
