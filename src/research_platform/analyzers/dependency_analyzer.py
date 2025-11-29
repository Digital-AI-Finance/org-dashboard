"""Dependency network analyzer.

Analyzes package dependencies across repositories to identify
shared dependencies, dependency clusters, and ecosystem patterns.
"""

import json
import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any

import networkx as nx

from ..models.repository import Repository


class DependencyAnalyzer:
    """Analyze dependency networks across repositories."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)
        self.graph = nx.DiGraph()

    def parse_requirements_txt(self, content: str) -> list[str]:
        """
        Parse requirements.txt content to extract package names.

        Args:
            content: Raw requirements.txt content

        Returns:
            List of package names
        """
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Skip -e editable installs
            if line.startswith("-e"):
                continue
            # Skip other pip options
            if line.startswith("-"):
                continue

            # Extract package name (before version specifier)
            # Handle formats: package==1.0, package>=1.0, package[extra]>=1.0
            match = re.match(r"^([a-zA-Z0-9_\-\.]+)", line)
            if match:
                package = match.group(1).lower()
                dependencies.append(package)

        return dependencies

    def parse_pyproject_toml(self, content: str) -> list[str]:
        """
        Parse pyproject.toml content to extract dependencies.

        Args:
            content: Raw pyproject.toml content

        Returns:
            List of package names
        """
        dependencies = []
        try:
            import tomli

            data = tomli.loads(content)

            # Check poetry dependencies
            if "tool" in data and "poetry" in data["tool"]:
                poetry_deps = data["tool"]["poetry"].get("dependencies", {})
                for dep in poetry_deps:
                    if dep != "python":  # Skip python version
                        dependencies.append(dep.lower())

            # Check project dependencies (PEP 621)
            if "project" in data:
                project_deps = data["project"].get("dependencies", [])
                for dep in project_deps:
                    match = re.match(r"^([a-zA-Z0-9_\-\.]+)", dep)
                    if match:
                        dependencies.append(match.group(1).lower())

        except Exception as e:
            self.logger.warning(f"Failed to parse pyproject.toml: {e}")

        return dependencies

    def parse_package_json(self, content: str) -> list[str]:
        """
        Parse package.json content to extract dependencies.

        Args:
            content: Raw package.json content

        Returns:
            List of package names
        """
        dependencies = []
        try:
            data = json.loads(content)

            # Regular dependencies
            if "dependencies" in data:
                dependencies.extend(data["dependencies"].keys())

            # Dev dependencies
            if "devDependencies" in data:
                dependencies.extend(data["devDependencies"].keys())

        except Exception as e:
            self.logger.warning(f"Failed to parse package.json: {e}")

        return dependencies

    def extract_repository_dependencies(self, repository: Repository) -> dict[str, list[str]]:
        """
        Extract all dependencies from a repository's metadata.

        Args:
            repository: Repository model with metadata

        Returns:
            Dictionary mapping file types to dependency lists
        """
        dependencies = {"requirements": [], "pyproject": [], "package": []}

        metadata = repository.metadata or {}

        # Parse requirements.txt if available
        if "requirements_txt" in metadata:
            dependencies["requirements"] = self.parse_requirements_txt(metadata["requirements_txt"])

        # Parse pyproject.toml if available
        if "pyproject_toml" in metadata:
            dependencies["pyproject"] = self.parse_pyproject_toml(metadata["pyproject_toml"])

        # Parse package.json if available
        if "package_json" in metadata:
            dependencies["package"] = self.parse_package_json(metadata["package_json"])

        return dependencies

    def build_dependency_graph(self, repositories: list[Repository]) -> nx.DiGraph:
        """
        Build a dependency network graph across all repositories.

        Args:
            repositories: List of repository models

        Returns:
            NetworkX directed graph of dependencies
        """
        self.graph.clear()

        for repo in repositories:
            deps = self.extract_repository_dependencies(repo)
            all_deps = deps["requirements"] + deps["pyproject"] + deps["package"]

            # Add repo node
            self.graph.add_node(
                repo.name,
                node_type="repository",
                full_name=repo.full_name,
                language=repo.language,
            )

            # Add dependency nodes and edges
            for dep in all_deps:
                if not self.graph.has_node(dep):
                    self.graph.add_node(dep, node_type="package")

                # Edge from repo to dependency
                if self.graph.has_edge(repo.name, dep):
                    self.graph[repo.name][dep]["weight"] += 1
                else:
                    self.graph.add_edge(repo.name, dep, weight=1)

        return self.graph

    def analyze_dependency_patterns(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Analyze dependency patterns across repositories.

        Args:
            repositories: List of repository models

        Returns:
            Dictionary with dependency analysis metrics
        """
        self.build_dependency_graph(repositories)

        # Count package usage across repos
        package_usage = Counter()
        repo_dependencies = {}

        for repo in repositories:
            deps = self.extract_repository_dependencies(repo)
            all_deps = set(deps["requirements"] + deps["pyproject"] + deps["package"])
            repo_dependencies[repo.name] = all_deps

            for dep in all_deps:
                package_usage[dep] += 1

        # Find shared dependencies
        shared_dependencies = {pkg: count for pkg, count in package_usage.items() if count > 1}

        # Calculate dependency overlap between repos
        overlap_matrix = {}
        repo_names = list(repo_dependencies.keys())
        for i, repo1 in enumerate(repo_names):
            for repo2 in repo_names[i + 1 :]:
                deps1 = repo_dependencies[repo1]
                deps2 = repo_dependencies[repo2]
                if deps1 or deps2:
                    overlap = len(deps1 & deps2)
                    if overlap > 0:
                        overlap_matrix[f"{repo1}-{repo2}"] = {
                            "overlap_count": overlap,
                            "shared_packages": list(deps1 & deps2),
                        }

        # Find dependency clusters (repos with similar dependencies)
        clusters = []
        if len(repo_names) >= 2:
            # Simple clustering: group repos that share many dependencies
            for repo in repo_names:
                cluster_members = [repo]
                repo_deps = repo_dependencies[repo]
                for other_repo in repo_names:
                    if other_repo != repo:
                        other_deps = repo_dependencies[other_repo]
                        if repo_deps and other_deps:
                            similarity = len(repo_deps & other_deps) / len(repo_deps | other_deps)
                            if similarity > 0.3:  # 30% similarity threshold
                                cluster_members.append(other_repo)
                if len(cluster_members) > 1:
                    clusters.append(cluster_members)

        # Remove duplicate clusters
        unique_clusters = []
        for cluster in clusters:
            cluster_set = set(cluster)
            if not any(cluster_set == set(c) for c in unique_clusters):
                unique_clusters.append(cluster)

        return {
            "total_repositories": len(repositories),
            "total_unique_packages": len(package_usage),
            "total_dependencies": sum(package_usage.values()),
            "most_common_packages": package_usage.most_common(20),
            "shared_dependencies": shared_dependencies,
            "dependency_overlap": overlap_matrix,
            "dependency_clusters": unique_clusters,
            "network_stats": {
                "nodes": self.graph.number_of_nodes(),
                "edges": self.graph.number_of_edges(),
                "density": (nx.density(self.graph) if self.graph.number_of_nodes() > 0 else 0),
            },
        }

    def get_repository_dependency_count(self, repositories: list[Repository]) -> dict[str, int]:
        """
        Get dependency count for each repository.

        Args:
            repositories: List of repository models

        Returns:
            Dictionary mapping repo names to dependency counts
        """
        counts = {}
        for repo in repositories:
            deps = self.extract_repository_dependencies(repo)
            all_deps = set(deps["requirements"] + deps["pyproject"] + deps["package"])
            counts[repo.name] = len(all_deps)
        return counts

    def save_dependency_report(self, analysis: dict[str, Any], output_path: Path) -> None:
        """
        Save dependency analysis report to JSON file.

        Args:
            analysis: Dependency analysis dictionary
            output_path: Path to save the JSON report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Dependency analysis report saved to {output_path}")


def analyze_all_dependencies(repos_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Standalone function to analyze dependencies for all repositories.

    Args:
        repos_data: List of repository dictionaries (from repos.json)

    Returns:
        Dependency analysis dictionary
    """
    repositories = [Repository.from_dict(repo_data) for repo_data in repos_data]

    analyzer = DependencyAnalyzer()
    return analyzer.analyze_dependency_patterns(repositories)


def generate_dependency_report(output_path: str | Path = "data/dependencies.json") -> None:
    """
    Generate dependency analysis report from existing repository data.

    Args:
        output_path: Path to save the report
    """
    repos_file = Path("data/repos.json")
    if not repos_file.exists():
        raise FileNotFoundError(f"Repository data not found: {repos_file}")

    with open(repos_file, encoding="utf-8") as f:
        repos_data = json.load(f)

    analysis = analyze_all_dependencies(repos_data)

    analyzer = DependencyAnalyzer()
    analyzer.save_dependency_report(analysis, Path(output_path))

    print("\nDependency Analysis Summary:")
    print(f"  - Total repositories: {analysis['total_repositories']}")
    print(f"  - Unique packages: {analysis['total_unique_packages']}")
    print(f"  - Total dependencies: {analysis['total_dependencies']}")
    print(f"  - Top 5 packages: {analysis['most_common_packages'][:5]}")


if __name__ == "__main__":
    generate_dependency_report()
