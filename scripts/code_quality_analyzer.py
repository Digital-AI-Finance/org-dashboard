#!/usr/bin/env python3
"""
Code quality metrics analyzer for Python repositories.
Analyzes code complexity, documentation, and structure.
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime
from typing import Any


class CodeQualityAnalyzer:
    """Analyze code quality metrics for repositories."""

    def __init__(self):
        self.metrics = {}

    def analyze_python_file(self, content: str, filepath: str) -> dict[str, Any]:
        """Analyze a single Python file for quality metrics."""
        metrics = {
            "lines_of_code": 0,
            "comment_lines": 0,
            "docstring_lines": 0,
            "blank_lines": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "complexity_score": 0,
        }

        lines = content.split("\n")
        in_docstring = False

        for line in lines:
            stripped = line.strip()

            # Blank lines
            if not stripped:
                metrics["blank_lines"] += 1
                continue

            # Docstrings
            if '"""' in line or "'''" in line:
                if not in_docstring:
                    in_docstring = True
                    metrics["docstring_lines"] += 1
                else:
                    metrics["docstring_lines"] += 1
                    in_docstring = False
                continue

            if in_docstring:
                metrics["docstring_lines"] += 1
                continue

            # Comments
            if stripped.startswith("#"):
                metrics["comment_lines"] += 1
                continue

            # Code lines
            metrics["lines_of_code"] += 1

            # Functions
            if re.match(r"^\s*def\s+\w+", line):
                metrics["functions"] += 1

            # Classes
            if re.match(r"^\s*class\s+\w+", line):
                metrics["classes"] += 1

            # Imports
            if re.match(r"^\s*(import|from)\s+", line):
                metrics["imports"] += 1

            # Complexity indicators
            if re.search(r"\b(if|for|while|try|except|with)\b", line):
                metrics["complexity_score"] += 1

        return metrics

    def calculate_quality_score(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Calculate overall quality score from metrics."""
        total_lines = (
            metrics["lines_of_code"]
            + metrics["comment_lines"]
            + metrics["docstring_lines"]
            + metrics["blank_lines"]
        )

        if total_lines == 0:
            return {"score": 0, "grade": "F"}

        # Documentation ratio (comments + docstrings / total)
        doc_ratio = (metrics["comment_lines"] + metrics["docstring_lines"]) / total_lines

        # Code organization (classes + functions)
        organization_score = min(100, (metrics["classes"] + metrics["functions"]) * 2)

        # Complexity penalty
        if metrics["lines_of_code"] > 0:
            complexity_ratio = metrics["complexity_score"] / metrics["lines_of_code"]
            complexity_penalty = max(0, (complexity_ratio - 0.3) * 100)
        else:
            complexity_penalty = 0

        # Overall score (0-100)
        score = (
            doc_ratio * 40  # 40% weight on documentation
            + min(organization_score, 40)  # 40% weight on organization
            + max(0, 20 - complexity_penalty)  # 20% weight on complexity
        )

        # Grade
        if score >= 80:
            grade = "A"
        elif score >= 70:
            grade = "B"
        elif score >= 60:
            grade = "C"
        elif score >= 50:
            grade = "D"
        else:
            grade = "F"

        return {
            "score": round(score, 2),
            "grade": grade,
            "documentation_ratio": round(doc_ratio * 100, 2),
            "organization_score": round(organization_score, 2),
            "complexity_ratio": round(complexity_ratio * 100, 2)
            if metrics["lines_of_code"] > 0
            else 0,
        }

    def analyze_repository_structure(self, repo_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze overall repository structure and quality."""
        # This would ideally fetch and analyze actual code files
        # For now, provide structure analysis based on available data

        structure_metrics = {
            "has_readme": bool(repo_data.get("description")),
            "has_license": repo_data.get("license") != "No License",
            "has_topics": len(repo_data.get("topics", [])) > 0,
            "has_description": bool(repo_data.get("description")),
            "recent_activity": True,  # Could check last_pushed
            "has_documentation": False,  # Would need to check for docs/
            "has_tests": False,  # Would need to check for tests/
            "has_ci": False,  # Would need to check for .github/workflows/
        }

        # Calculate structure score
        score = sum(
            [
                structure_metrics["has_readme"] * 20,
                structure_metrics["has_license"] * 15,
                structure_metrics["has_topics"] * 10,
                structure_metrics["has_description"] * 10,
                structure_metrics["recent_activity"] * 10,
                structure_metrics["has_documentation"] * 15,
                structure_metrics["has_tests"] * 15,
                structure_metrics["has_ci"] * 15,
            ]
        )

        return {
            "structure_score": score,
            "max_score": 100,
            "metrics": structure_metrics,
            "grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D",
        }


def analyze_all_repositories(repos_data: list[dict]) -> dict[str, Any]:
    """Analyze code quality for all repositories."""
    print("Analyzing code quality...")

    analyzer = CodeQualityAnalyzer()
    quality_report = {"generated_at": datetime.now().isoformat(), "repositories": {}}

    for repo in repos_data:
        repo_name = repo["name"]
        print(f"  Analyzing {repo_name}...")

        structure_analysis = analyzer.analyze_repository_structure(repo)

        quality_report["repositories"][repo_name] = {
            "structure": structure_analysis,
            "language": repo.get("language", "Unknown"),
            "size_kb": repo.get("size_kb", 0),
        }

    # Organization-wide summary
    avg_structure_score = (
        sum(r["structure"]["structure_score"] for r in quality_report["repositories"].values())
        / len(repos_data)
        if repos_data
        else 0
    )

    quality_report["summary"] = {
        "total_repositories": len(repos_data),
        "average_structure_score": round(avg_structure_score, 2),
        "grades": defaultdict(int),
    }

    for repo_data in quality_report["repositories"].values():
        grade = repo_data["structure"]["grade"]
        quality_report["summary"]["grades"][grade] += 1

    # Save report
    output_path = "data/code_quality_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(quality_report, f, indent=2, ensure_ascii=False)

    print(f"Code quality report saved to {output_path}")
    return quality_report


def main():
    """Test code quality analyzer."""
    print("Code Quality Analyzer")
    print("=" * 60)

    if os.path.exists("data/repos.json"):
        with open("data/repos.json", encoding="utf-8") as f:
            repos_data = json.load(f)

        report = analyze_all_repositories(repos_data)

        print("\nSummary:")
        print(f"  Total repositories: {report['summary']['total_repositories']}")
        print(f"  Average structure score: {report['summary']['average_structure_score']}/100")
        print(f"  Grade distribution: {dict(report['summary']['grades'])}")

    else:
        print("No repos data found. Run build_research_platform.py first.")


if __name__ == "__main__":
    from datetime import datetime

    main()
