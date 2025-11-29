"""Tests for DependencyAnalyzer."""

import json

import pytest

from research_platform.analyzers.dependency_analyzer import DependencyAnalyzer
from research_platform.models.repository import Repository


@pytest.fixture
def dependency_analyzer():
    """Create DependencyAnalyzer instance."""
    return DependencyAnalyzer()


@pytest.fixture
def sample_requirements_txt():
    """Sample requirements.txt content."""
    return """# Core dependencies
numpy==1.24.0
pandas>=2.0.0
matplotlib<4.0

# Optional extras
scipy[optimize]>=1.10.0

# Editable install (should be skipped)
-e git+https://github.com/example/repo.git#egg=example

# Pip options (should be skipped)
--index-url https://pypi.org/simple
-r other-requirements.txt

requests
plotly==5.14.1
"""


@pytest.fixture
def sample_pyproject_toml():
    """Sample pyproject.toml content."""
    return """[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
numpy = "^1.24.0"
pandas = "^2.0.0"
requests = "*"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"

[project]
dependencies = [
    "matplotlib>=3.5.0",
    "scipy>=1.10.0",
]
"""


@pytest.fixture
def sample_package_json():
    """Sample package.json content."""
    return """{
  "name": "test-package",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0",
    "axios": "^1.4.0",
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "webpack": "^5.88.0"
  }
}"""


@pytest.fixture
def repo_with_python_deps():
    """Create repository with Python dependencies."""
    return Repository(
        id=1,
        name="python-repo",
        full_name="org/python-repo",
        language="Python",
        metadata={
            "requirements_txt": "numpy==1.24.0\npandas>=2.0.0\nrequests\n",
        },
    )


@pytest.fixture
def repo_with_js_deps():
    """Create repository with JavaScript dependencies."""
    return Repository(
        id=2,
        name="js-repo",
        full_name="org/js-repo",
        language="JavaScript",
        metadata={
            "package_json": '{"dependencies": {"react": "^18.0.0", "axios": "^1.4.0"}}',
        },
    )


@pytest.fixture
def repo_without_deps():
    """Create repository without dependencies."""
    return Repository(
        id=3,
        name="no-deps",
        full_name="org/no-deps",
        language="Python",
        metadata={},
    )


class TestDependencyAnalyzer:
    """Tests for DependencyAnalyzer functionality."""

    def test_parse_requirements_txt_basic(self, dependency_analyzer, sample_requirements_txt):
        """Test parsing basic requirements.txt."""
        deps = dependency_analyzer.parse_requirements_txt(sample_requirements_txt)

        assert "numpy" in deps
        assert "pandas" in deps
        assert "matplotlib" in deps
        assert "scipy" in deps
        assert "requests" in deps
        assert "plotly" in deps

    def test_parse_requirements_txt_skips_comments(self, dependency_analyzer):
        """Test that comments are skipped."""
        content = "# This is a comment\nnumpy==1.24.0\n# Another comment\npandas\n"
        deps = dependency_analyzer.parse_requirements_txt(content)

        assert len(deps) == 2
        assert "numpy" in deps
        assert "pandas" in deps

    def test_parse_requirements_txt_skips_editable(self, dependency_analyzer):
        """Test that editable installs are skipped."""
        content = "-e git+https://github.com/example/repo.git#egg=example\nnumpy\n"
        deps = dependency_analyzer.parse_requirements_txt(content)

        assert len(deps) == 1
        assert "numpy" in deps
        assert "example" not in deps

    def test_parse_requirements_txt_skips_options(self, dependency_analyzer):
        """Test that pip options are skipped."""
        content = "--index-url https://pypi.org/simple\n-r other.txt\nnumpy\n"
        deps = dependency_analyzer.parse_requirements_txt(content)

        assert len(deps) == 1
        assert "numpy" in deps

    def test_parse_requirements_txt_empty(self, dependency_analyzer):
        """Test parsing empty requirements.txt."""
        deps = dependency_analyzer.parse_requirements_txt("")
        assert deps == []

    def test_parse_requirements_txt_normalizes_case(self, dependency_analyzer):
        """Test that package names are normalized to lowercase."""
        content = "NumPy==1.24.0\nPANDAS>=2.0.0\n"
        deps = dependency_analyzer.parse_requirements_txt(content)

        assert "numpy" in deps
        assert "pandas" in deps
        assert "NumPy" not in deps
        assert "PANDAS" not in deps

    def test_parse_pyproject_toml_poetry(self, dependency_analyzer, sample_pyproject_toml):
        """Test parsing pyproject.toml with poetry dependencies."""
        pytest.importorskip("tomli")
        deps = dependency_analyzer.parse_pyproject_toml(sample_pyproject_toml)

        assert "numpy" in deps
        assert "pandas" in deps
        assert "requests" in deps
        assert "python" not in deps  # Should skip python version

    def test_parse_pyproject_toml_pep621(self, dependency_analyzer):
        """Test parsing pyproject.toml with PEP 621 format."""
        pytest.importorskip("tomli")
        content = """[project]
dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
]
"""
        deps = dependency_analyzer.parse_pyproject_toml(content)

        assert "numpy" in deps
        assert "pandas" in deps

    def test_parse_pyproject_toml_empty(self, dependency_analyzer):
        """Test parsing empty pyproject.toml."""
        pytest.importorskip("tomli")
        deps = dependency_analyzer.parse_pyproject_toml("[tool.other]\nvalue = 1")
        assert deps == []

    def test_parse_pyproject_toml_invalid(self, dependency_analyzer):
        """Test parsing invalid TOML."""
        deps = dependency_analyzer.parse_pyproject_toml("not valid toml {{{")
        assert deps == []

    def test_parse_pyproject_toml_missing_tomli(self, dependency_analyzer, monkeypatch):
        """Test handling when tomli is not available."""
        # This test simulates tomli not being available
        import sys

        with monkeypatch.context() as m:
            m.setitem(sys.modules, "tomli", None)
            # Should handle gracefully when tomli import fails
            deps = dependency_analyzer.parse_pyproject_toml("[tool.poetry]\nname='test'")
            assert isinstance(deps, list)

    def test_parse_package_json_basic(self, dependency_analyzer, sample_package_json):
        """Test parsing package.json."""
        deps = dependency_analyzer.parse_package_json(sample_package_json)

        assert "react" in deps
        assert "axios" in deps
        assert "lodash" in deps
        assert "jest" in deps  # Dev dependencies included
        assert "webpack" in deps

    def test_parse_package_json_only_regular_deps(self, dependency_analyzer):
        """Test parsing package.json with only regular dependencies."""
        content = '{"dependencies": {"react": "^18.0.0", "axios": "^1.4.0"}}'
        deps = dependency_analyzer.parse_package_json(content)

        assert len(deps) == 2
        assert "react" in deps
        assert "axios" in deps

    def test_parse_package_json_only_dev_deps(self, dependency_analyzer):
        """Test parsing package.json with only dev dependencies."""
        content = '{"devDependencies": {"jest": "^29.0.0"}}'
        deps = dependency_analyzer.parse_package_json(content)

        assert len(deps) == 1
        assert "jest" in deps

    def test_parse_package_json_empty(self, dependency_analyzer):
        """Test parsing empty package.json."""
        deps = dependency_analyzer.parse_package_json("{}")
        assert deps == []

    def test_parse_package_json_invalid(self, dependency_analyzer):
        """Test parsing invalid JSON."""
        deps = dependency_analyzer.parse_package_json("not valid json")
        assert deps == []

    def test_extract_repository_dependencies(self, dependency_analyzer, repo_with_python_deps):
        """Test extracting dependencies from repository."""
        deps = dependency_analyzer.extract_repository_dependencies(repo_with_python_deps)

        assert "requirements" in deps
        assert "pyproject" in deps
        assert "package" in deps
        assert "numpy" in deps["requirements"]
        assert "pandas" in deps["requirements"]
        assert "requests" in deps["requirements"]

    def test_extract_repository_dependencies_no_metadata(
        self, dependency_analyzer, repo_without_deps
    ):
        """Test extracting dependencies from repo without metadata."""
        deps = dependency_analyzer.extract_repository_dependencies(repo_without_deps)

        assert deps["requirements"] == []
        assert deps["pyproject"] == []
        assert deps["package"] == []

    def test_extract_repository_dependencies_js(self, dependency_analyzer, repo_with_js_deps):
        """Test extracting JavaScript dependencies."""
        deps = dependency_analyzer.extract_repository_dependencies(repo_with_js_deps)

        assert "react" in deps["package"]
        assert "axios" in deps["package"]

    def test_build_dependency_graph_single_repo(self, dependency_analyzer, repo_with_python_deps):
        """Test building dependency graph with single repository."""
        graph = dependency_analyzer.build_dependency_graph([repo_with_python_deps])

        # Check repository node exists
        assert "python-repo" in graph.nodes()
        assert graph.nodes["python-repo"]["node_type"] == "repository"

        # Check package nodes exist
        assert "numpy" in graph.nodes()
        assert "pandas" in graph.nodes()
        assert "requests" in graph.nodes()

        # Check edges from repo to packages
        assert graph.has_edge("python-repo", "numpy")
        assert graph.has_edge("python-repo", "pandas")
        assert graph.has_edge("python-repo", "requests")

    def test_build_dependency_graph_multiple_repos(
        self, dependency_analyzer, repo_with_python_deps, repo_with_js_deps
    ):
        """Test building dependency graph with multiple repositories."""
        graph = dependency_analyzer.build_dependency_graph(
            [repo_with_python_deps, repo_with_js_deps]
        )

        # Check both repos
        assert "python-repo" in graph.nodes()
        assert "js-repo" in graph.nodes()

        # Check all packages
        assert "numpy" in graph.nodes()
        assert "react" in graph.nodes()

    def test_build_dependency_graph_shared_deps(self, dependency_analyzer):
        """Test that shared dependencies are tracked correctly."""
        repo1 = Repository(
            id=1,
            name="repo1",
            full_name="org/repo1",
            metadata={"requirements_txt": "numpy\npandas\n"},
        )
        repo2 = Repository(
            id=2,
            name="repo2",
            full_name="org/repo2",
            metadata={"requirements_txt": "numpy\nmatplotlib\n"},
        )

        graph = dependency_analyzer.build_dependency_graph([repo1, repo2])

        # Both repos should have edges to numpy
        assert graph.has_edge("repo1", "numpy")
        assert graph.has_edge("repo2", "numpy")

    def test_analyze_dependency_patterns(
        self, dependency_analyzer, repo_with_python_deps, repo_with_js_deps, repo_without_deps
    ):
        """Test analyzing dependency patterns across repos."""
        analysis = dependency_analyzer.analyze_dependency_patterns(
            [repo_with_python_deps, repo_with_js_deps, repo_without_deps]
        )

        assert analysis["total_repositories"] == 3
        assert analysis["total_unique_packages"] > 0
        assert "most_common_packages" in analysis
        assert "shared_dependencies" in analysis
        assert "network_stats" in analysis

    def test_analyze_dependency_patterns_finds_common_packages(self, dependency_analyzer):
        """Test that common packages are identified."""
        repo1 = Repository(
            id=1,
            name="repo1",
            full_name="org/repo1",
            metadata={"requirements_txt": "numpy\npandas\n"},
        )
        repo2 = Repository(
            id=2,
            name="repo2",
            full_name="org/repo2",
            metadata={"requirements_txt": "numpy\nmatplotlib\n"},
        )

        analysis = dependency_analyzer.analyze_dependency_patterns([repo1, repo2])

        # numpy should be in shared dependencies (used by 2 repos)
        assert "numpy" in analysis["shared_dependencies"]
        assert analysis["shared_dependencies"]["numpy"] == 2

        # pandas and matplotlib should not be shared (used by 1 repo each)
        assert "pandas" not in analysis["shared_dependencies"]
        assert "matplotlib" not in analysis["shared_dependencies"]

    def test_analyze_dependency_patterns_overlap_matrix(self, dependency_analyzer):
        """Test dependency overlap matrix calculation."""
        repo1 = Repository(
            id=1,
            name="repo1",
            full_name="org/repo1",
            metadata={"requirements_txt": "numpy\npandas\nmatplotlib\n"},
        )
        repo2 = Repository(
            id=2,
            name="repo2",
            full_name="org/repo2",
            metadata={"requirements_txt": "numpy\npandas\nscipy\n"},
        )

        analysis = dependency_analyzer.analyze_dependency_patterns([repo1, repo2])

        overlap = analysis["dependency_overlap"]
        assert "repo1-repo2" in overlap
        assert overlap["repo1-repo2"]["overlap_count"] == 2  # numpy, pandas
        assert set(overlap["repo1-repo2"]["shared_packages"]) == {"numpy", "pandas"}

    def test_analyze_dependency_patterns_empty_repos(self, dependency_analyzer):
        """Test analysis with repositories without dependencies."""
        repo1 = Repository(id=1, name="repo1", full_name="org/repo1", metadata={})
        repo2 = Repository(id=2, name="repo2", full_name="org/repo2", metadata={})

        analysis = dependency_analyzer.analyze_dependency_patterns([repo1, repo2])

        assert analysis["total_unique_packages"] == 0
        assert analysis["total_dependencies"] == 0
        assert analysis["most_common_packages"] == []

    def test_get_repository_dependency_count(
        self, dependency_analyzer, repo_with_python_deps, repo_without_deps
    ):
        """Test getting dependency counts per repository."""
        counts = dependency_analyzer.get_repository_dependency_count(
            [repo_with_python_deps, repo_without_deps]
        )

        assert counts["python-repo"] == 3  # numpy, pandas, requests
        assert counts["no-deps"] == 0

    def test_get_repository_dependency_count_deduplicates(self, dependency_analyzer):
        """Test that dependency counts deduplicate packages."""
        repo = Repository(
            id=1,
            name="repo1",
            full_name="org/repo1",
            metadata={
                "requirements_txt": "numpy\npandas\n",
                "pyproject_toml": '[project]\ndependencies = ["numpy>=1.0"]',
            },
        )

        pytest.importorskip("tomli")
        counts = dependency_analyzer.get_repository_dependency_count([repo])

        # numpy appears in both files but should be counted once
        assert counts["repo1"] == 2  # numpy, pandas (numpy deduplicated)

    def test_save_dependency_report(self, dependency_analyzer, temp_dir):
        """Test saving dependency report to JSON file."""
        analysis = {
            "total_repositories": 5,
            "total_unique_packages": 20,
            "most_common_packages": [("numpy", 3), ("pandas", 2)],
        }

        output_path = temp_dir / "dependencies.json"
        dependency_analyzer.save_dependency_report(analysis, output_path)

        assert output_path.exists()

        # Verify content
        with open(output_path, encoding="utf-8") as f:
            loaded_data = json.load(f)

        assert loaded_data["total_repositories"] == 5
        assert loaded_data["total_unique_packages"] == 20

    def test_network_stats_calculation(self, dependency_analyzer, repo_with_python_deps):
        """Test network statistics calculation."""
        analysis = dependency_analyzer.analyze_dependency_patterns([repo_with_python_deps])

        stats = analysis["network_stats"]
        assert "nodes" in stats
        assert "edges" in stats
        assert "density" in stats
        assert stats["nodes"] > 0
        assert stats["edges"] > 0

    def test_dependency_clusters_detection(self, dependency_analyzer):
        """Test detection of dependency clusters."""
        # Create repos with similar dependencies
        repo1 = Repository(
            id=1,
            name="ml-repo1",
            full_name="org/ml-repo1",
            metadata={"requirements_txt": "numpy\npandas\nscipy\nscikit-learn\n"},
        )
        repo2 = Repository(
            id=2,
            name="ml-repo2",
            full_name="org/ml-repo2",
            metadata={"requirements_txt": "numpy\npandas\nscipy\ntensorflow\n"},
        )
        repo3 = Repository(
            id=3,
            name="web-repo",
            full_name="org/web-repo",
            metadata={"package_json": '{"dependencies": {"react": "18.0", "axios": "1.0"}}'},
        )

        analysis = dependency_analyzer.analyze_dependency_patterns([repo1, repo2, repo3])

        clusters = analysis["dependency_clusters"]
        # ml-repo1 and ml-repo2 should be in a cluster (share numpy, pandas, scipy)
        assert len(clusters) > 0

    def test_parse_requirements_txt_with_extras(self, dependency_analyzer):
        """Test parsing requirements with extras (e.g., package[extra])."""
        content = "scipy[optimize]>=1.10.0\ndjango[postgresql]>=4.0\n"
        deps = dependency_analyzer.parse_requirements_txt(content)

        assert "scipy" in deps
        assert "django" in deps

    def test_graph_clears_between_builds(self, dependency_analyzer, repo_with_python_deps):
        """Test that graph is cleared between builds."""
        # First build
        graph1 = dependency_analyzer.build_dependency_graph([repo_with_python_deps])
        node_count1 = graph1.number_of_nodes()

        # Second build with different data
        repo2 = Repository(
            id=2, name="repo2", full_name="org/repo2", metadata={"requirements_txt": "numpy\n"}
        )
        graph2 = dependency_analyzer.build_dependency_graph([repo2])

        # Should have fewer nodes (only repo2 and numpy)
        assert graph2.number_of_nodes() < node_count1
        assert "python-repo" not in graph2.nodes()
        assert "repo2" in graph2.nodes()
