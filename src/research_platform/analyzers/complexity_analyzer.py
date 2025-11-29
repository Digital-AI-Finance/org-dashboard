"""Code complexity analyzer using radon.

Analyzes code complexity metrics including cyclomatic complexity,
maintainability index, and raw metrics for Python code.
"""

import json
import logging
from pathlib import Path
from typing import Any

from ..models.repository import Repository


class ComplexityAnalyzer:
    """Analyze code complexity metrics across repositories."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)

    def calculate_cyclomatic_complexity(self, code: str, filename: str = "temp.py") -> list[dict]:
        """
        Calculate cyclomatic complexity for Python code.

        Args:
            code: Python source code string
            filename: Name for the code block

        Returns:
            List of complexity results per function/class
        """
        try:
            from radon.complexity import cc_visit

            results = cc_visit(code, no_assert=True)
            return [
                {
                    "name": result.name,
                    "type": result.type,
                    "complexity": result.complexity,
                    "lineno": result.lineno,
                    "rank": result.letter,
                }
                for result in results
            ]
        except ImportError:
            self.logger.warning("radon not installed, skipping complexity analysis")
            return []
        except Exception as e:
            self.logger.warning(f"Error calculating complexity for {filename}: {e}")
            return []

    def calculate_maintainability_index(self, code: str) -> float | None:
        """
        Calculate maintainability index for Python code.

        Args:
            code: Python source code string

        Returns:
            Maintainability index (0-100) or None if calculation fails
        """
        try:
            from radon.metrics import mi_visit

            mi = mi_visit(code, multi=True)
            if mi:
                return round(mi, 2)
            return None
        except ImportError:
            return None
        except Exception as e:
            self.logger.warning(f"Error calculating maintainability index: {e}")
            return None

    def calculate_raw_metrics(self, code: str) -> dict[str, int]:
        """
        Calculate raw metrics (LOC, LLOC, comments, etc.).

        Args:
            code: Python source code string

        Returns:
            Dictionary with raw metrics
        """
        try:
            from radon.raw import analyze

            analysis = analyze(code)
            return {
                "loc": analysis.loc,  # Lines of code
                "lloc": analysis.lloc,  # Logical lines of code
                "sloc": analysis.sloc,  # Source lines of code
                "comments": analysis.comments,
                "multi": analysis.multi,  # Multi-line strings
                "blank": analysis.blank,
            }
        except ImportError:
            return {"loc": 0, "lloc": 0, "sloc": 0, "comments": 0, "multi": 0, "blank": 0}
        except Exception as e:
            self.logger.warning(f"Error calculating raw metrics: {e}")
            return {"loc": 0, "lloc": 0, "sloc": 0, "comments": 0, "multi": 0, "blank": 0}

    def analyze_code_file(self, code: str, filename: str) -> dict[str, Any]:
        """
        Comprehensive analysis of a single code file.

        Args:
            code: Python source code
            filename: Name of the file

        Returns:
            Dictionary with all complexity metrics
        """
        cc_results = self.calculate_cyclomatic_complexity(code, filename)
        mi = self.calculate_maintainability_index(code)
        raw = self.calculate_raw_metrics(code)

        # Calculate average complexity
        avg_complexity = 0.0
        max_complexity = 0
        if cc_results:
            complexities = [r["complexity"] for r in cc_results]
            avg_complexity = sum(complexities) / len(complexities)
            max_complexity = max(complexities)

        return {
            "filename": filename,
            "cyclomatic_complexity": cc_results,
            "average_complexity": round(avg_complexity, 2),
            "max_complexity": max_complexity,
            "maintainability_index": mi,
            "raw_metrics": raw,
            "total_functions": len(cc_results),
            "complex_functions": len([r for r in cc_results if r["complexity"] > 10]),
        }

    def analyze_repository_complexity(self, repository: Repository) -> dict[str, Any]:
        """
        Analyze complexity metrics for a repository.

        Args:
            repository: Repository model with code metadata

        Returns:
            Dictionary with repository complexity metrics
        """
        metadata = repository.metadata or {}
        code_files = metadata.get("code_files", {})

        if not code_files or not isinstance(code_files, dict):
            return {
                "repository": repository.name,
                "language": repository.language,
                "has_code_analysis": False,
                "total_files": 0,
                "total_loc": 0,
                "total_functions": 0,
                "average_complexity": 0.0,
                "average_maintainability": 0.0,
            }

        file_analyses = []
        for filename, code in code_files.items():
            if filename.endswith(".py"):  # Only analyze Python files
                analysis = self.analyze_code_file(code, filename)
                file_analyses.append(analysis)

        if not file_analyses:
            return {
                "repository": repository.name,
                "language": repository.language,
                "has_code_analysis": False,
                "total_files": 0,
                "total_loc": 0,
                "total_functions": 0,
                "average_complexity": 0.0,
                "average_maintainability": 0.0,
            }

        # Aggregate metrics
        total_loc = sum(f["raw_metrics"]["loc"] for f in file_analyses)
        total_functions = sum(f["total_functions"] for f in file_analyses)
        total_complex_functions = sum(f["complex_functions"] for f in file_analyses)

        # Calculate averages
        all_complexities = []
        all_maintainability = []
        for f in file_analyses:
            if f["average_complexity"] > 0:
                all_complexities.append(f["average_complexity"])
            if f["maintainability_index"] is not None:
                all_maintainability.append(f["maintainability_index"])

        avg_complexity = sum(all_complexities) / len(all_complexities) if all_complexities else 0.0
        avg_maintainability = (
            sum(all_maintainability) / len(all_maintainability) if all_maintainability else 0.0
        )

        return {
            "repository": repository.name,
            "language": repository.language,
            "has_code_analysis": True,
            "total_files": len(file_analyses),
            "total_loc": total_loc,
            "total_functions": total_functions,
            "complex_functions": total_complex_functions,
            "average_complexity": round(avg_complexity, 2),
            "average_maintainability": round(avg_maintainability, 2),
            "file_analyses": file_analyses,
            "most_complex_files": sorted(
                file_analyses, key=lambda x: x["max_complexity"], reverse=True
            )[:5],
        }

    def analyze_organization_complexity(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Analyze code complexity across all repositories.

        Args:
            repositories: List of repository models

        Returns:
            Dictionary with organization-wide complexity metrics
        """
        repo_analyses = []
        total_files = 0
        total_loc = 0
        total_functions = 0
        total_complex_functions = 0

        for repo in repositories:
            analysis = self.analyze_repository_complexity(repo)
            if analysis["has_code_analysis"]:
                repo_analyses.append(analysis)
                total_files += analysis["total_files"]
                total_loc += analysis["total_loc"]
                total_functions += analysis["total_functions"]
                total_complex_functions += analysis["complex_functions"]

        # Calculate averages
        all_complexities = [
            r["average_complexity"] for r in repo_analyses if r["average_complexity"] > 0
        ]
        all_maintainability = [
            r["average_maintainability"] for r in repo_analyses if r["average_maintainability"] > 0
        ]

        avg_complexity = sum(all_complexities) / len(all_complexities) if all_complexities else 0.0
        avg_maintainability = (
            sum(all_maintainability) / len(all_maintainability) if all_maintainability else 0.0
        )

        return {
            "organization_metrics": {
                "total_repositories": len(repositories),
                "repositories_analyzed": len(repo_analyses),
                "total_files": total_files,
                "total_loc": total_loc,
                "total_functions": total_functions,
                "complex_functions": total_complex_functions,
                "average_complexity": round(avg_complexity, 2),
                "average_maintainability": round(avg_maintainability, 2),
            },
            "repository_analyses": repo_analyses,
            "most_complex_repositories": sorted(
                repo_analyses, key=lambda x: x["average_complexity"], reverse=True
            )[:10],
            "most_maintainable_repositories": sorted(
                repo_analyses, key=lambda x: x["average_maintainability"], reverse=True
            )[:10],
        }

    def save_complexity_report(self, analysis: dict[str, Any], output_path: Path) -> None:
        """
        Save complexity analysis report to JSON file.

        Args:
            analysis: Complexity analysis dictionary
            output_path: Path to save the JSON report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Complexity analysis report saved to {output_path}")


def analyze_all_complexity(repos_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Standalone function to analyze complexity for all repositories.

    Args:
        repos_data: List of repository dictionaries (from repos.json)

    Returns:
        Complexity analysis dictionary
    """
    repositories = [Repository.from_dict(repo_data) for repo_data in repos_data]

    analyzer = ComplexityAnalyzer()
    return analyzer.analyze_organization_complexity(repositories)


def generate_complexity_report(output_path: str | Path = "data/complexity.json") -> None:
    """
    Generate complexity analysis report from existing repository data.

    Args:
        output_path: Path to save the report
    """
    repos_file = Path("data/repos.json")
    if not repos_file.exists():
        raise FileNotFoundError(f"Repository data not found: {repos_file}")

    with open(repos_file, encoding="utf-8") as f:
        repos_data = json.load(f)

    analysis = analyze_all_complexity(repos_data)

    analyzer = ComplexityAnalyzer()
    analyzer.save_complexity_report(analysis, Path(output_path))

    print("\nCode Complexity Summary:")
    print(f"  - Repositories analyzed: {analysis['organization_metrics']['repositories_analyzed']}")
    print(f"  - Total files: {analysis['organization_metrics']['total_files']}")
    print(f"  - Total LOC: {analysis['organization_metrics']['total_loc']}")
    print(f"  - Average complexity: {analysis['organization_metrics']['average_complexity']}")
    print(
        f"  - Average maintainability: {analysis['organization_metrics']['average_maintainability']}"
    )


if __name__ == "__main__":
    generate_complexity_report()
