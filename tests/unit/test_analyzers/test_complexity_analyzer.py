"""Tests for ComplexityAnalyzer."""

import json

import pytest

from research_platform.analyzers.complexity_analyzer import ComplexityAnalyzer
from research_platform.models.repository import Repository


@pytest.fixture
def complexity_analyzer():
    """Create ComplexityAnalyzer instance."""
    return ComplexityAnalyzer()


@pytest.fixture
def simple_python_code():
    """Simple Python function for testing."""
    return """
def add(a, b):
    return a + b

def multiply(x, y):
    return x * y
"""


@pytest.fixture
def complex_python_code():
    """Complex Python function with high cyclomatic complexity."""
    return """
def complex_function(a, b, c):
    if a > 0:
        if b > 0:
            if c > 0:
                return a + b + c
            else:
                return a + b - c
        else:
            if c > 0:
                return a - b + c
            else:
                return a - b - c
    else:
        if b > 0:
            if c > 0:
                return -a + b + c
            else:
                return -a + b - c
        else:
            if c > 0:
                return -a - b + c
            else:
                return -a - b - c
"""


@pytest.fixture
def repo_with_code():
    """Repository with Python code."""
    return Repository(
        id=1,
        name="code-repo",
        full_name="org/code-repo",
        language="Python",
        metadata={
            "code_files": {
                "main.py": "def hello():\n    return 'world'\n",
                "utils.py": "def add(a, b):\n    return a + b\n",
            }
        },
    )


@pytest.fixture
def repo_without_code():
    """Repository without code files."""
    return Repository(
        id=2,
        name="no-code",
        full_name="org/no-code",
        language="Python",
        metadata={},
    )


class TestComplexityAnalyzer:
    """Tests for ComplexityAnalyzer functionality."""

    def test_calculate_cyclomatic_complexity_simple(self, complexity_analyzer, simple_python_code):
        """Test cyclomatic complexity calculation for simple code."""
        pytest.importorskip("radon")
        results = complexity_analyzer.calculate_cyclomatic_complexity(simple_python_code, "test.py")

        assert len(results) == 2
        assert results[0]["name"] == "add"
        assert results[0]["type"] == "function"
        assert results[0]["complexity"] == 1  # Simple function
        assert "rank" in results[0]

    def test_calculate_cyclomatic_complexity_complex(
        self, complexity_analyzer, complex_python_code
    ):
        """Test cyclomatic complexity for complex code."""
        pytest.importorskip("radon")
        results = complexity_analyzer.calculate_cyclomatic_complexity(
            complex_python_code, "complex.py"
        )

        assert len(results) == 1
        assert results[0]["name"] == "complex_function"
        # This function has many nested if statements
        assert results[0]["complexity"] > 10

    def test_calculate_cyclomatic_complexity_empty(self, complexity_analyzer):
        """Test cyclomatic complexity for empty code."""
        pytest.importorskip("radon")
        results = complexity_analyzer.calculate_cyclomatic_complexity("", "empty.py")
        assert results == []

    def test_calculate_cyclomatic_complexity_invalid_syntax(self, complexity_analyzer):
        """Test handling of invalid Python syntax."""
        pytest.importorskip("radon")
        results = complexity_analyzer.calculate_cyclomatic_complexity(
            "def invalid syntax {{{", "invalid.py"
        )
        assert results == []

    def test_calculate_cyclomatic_complexity_without_radon(self, complexity_analyzer, monkeypatch):
        """Test handling when radon is not available."""
        import sys

        with monkeypatch.context() as m:
            m.setitem(sys.modules, "radon", None)
            m.setitem(sys.modules, "radon.complexity", None)
            results = complexity_analyzer.calculate_cyclomatic_complexity(
                "def test(): pass", "test.py"
            )
            assert results == []

    def test_calculate_maintainability_index(self, complexity_analyzer, simple_python_code):
        """Test maintainability index calculation."""
        pytest.importorskip("radon")
        mi = complexity_analyzer.calculate_maintainability_index(simple_python_code)

        assert mi is not None
        assert 0 <= mi <= 100
        # Simple code should have high maintainability
        assert mi > 50

    def test_calculate_maintainability_index_complex(
        self, complexity_analyzer, complex_python_code
    ):
        """Test maintainability index for complex code."""
        pytest.importorskip("radon")
        mi = complexity_analyzer.calculate_maintainability_index(complex_python_code)

        assert mi is not None
        # Complex code should have lower maintainability
        assert mi < 100

    def test_calculate_maintainability_index_empty(self, complexity_analyzer):
        """Test maintainability index for empty code."""
        pytest.importorskip("radon")
        mi = complexity_analyzer.calculate_maintainability_index("")
        # Empty code might return None or a specific value
        assert mi is None or isinstance(mi, int | float)

    def test_calculate_maintainability_index_invalid(self, complexity_analyzer):
        """Test maintainability index for invalid code."""
        pytest.importorskip("radon")
        mi = complexity_analyzer.calculate_maintainability_index("def invalid {{{")
        assert mi is None

    def test_calculate_raw_metrics(self, complexity_analyzer, simple_python_code):
        """Test raw metrics calculation."""
        pytest.importorskip("radon")
        metrics = complexity_analyzer.calculate_raw_metrics(simple_python_code)

        assert "loc" in metrics
        assert "lloc" in metrics
        assert "sloc" in metrics
        assert "comments" in metrics
        assert "multi" in metrics
        assert "blank" in metrics
        assert metrics["loc"] > 0
        assert metrics["sloc"] > 0

    def test_calculate_raw_metrics_with_comments(self, complexity_analyzer):
        """Test raw metrics with comments."""
        pytest.importorskip("radon")
        code = """# This is a comment
def test():
    # Another comment
    return True
"""
        metrics = complexity_analyzer.calculate_raw_metrics(code)

        assert metrics["comments"] >= 2
        assert metrics["loc"] > metrics["sloc"]

    def test_calculate_raw_metrics_empty(self, complexity_analyzer):
        """Test raw metrics for empty code."""
        pytest.importorskip("radon")
        metrics = complexity_analyzer.calculate_raw_metrics("")

        assert metrics["loc"] == 0
        assert metrics["sloc"] == 0

    def test_calculate_raw_metrics_without_radon(self, complexity_analyzer, monkeypatch):
        """Test raw metrics when radon is not available."""
        import sys

        with monkeypatch.context() as m:
            m.setitem(sys.modules, "radon", None)
            m.setitem(sys.modules, "radon.raw", None)
            metrics = complexity_analyzer.calculate_raw_metrics("def test(): pass")

            assert metrics["loc"] == 0
            assert metrics["lloc"] == 0

    def test_analyze_code_file(self, complexity_analyzer, simple_python_code):
        """Test comprehensive file analysis."""
        pytest.importorskip("radon")
        analysis = complexity_analyzer.analyze_code_file(simple_python_code, "simple.py")

        assert analysis["filename"] == "simple.py"
        assert "cyclomatic_complexity" in analysis
        assert "average_complexity" in analysis
        assert "max_complexity" in analysis
        assert "maintainability_index" in analysis
        assert "raw_metrics" in analysis
        assert "total_functions" in analysis
        assert "complex_functions" in analysis
        assert analysis["total_functions"] == 2

    def test_analyze_code_file_complex_functions(self, complexity_analyzer, complex_python_code):
        """Test analysis identifies complex functions."""
        pytest.importorskip("radon")
        analysis = complexity_analyzer.analyze_code_file(complex_python_code, "complex.py")

        assert analysis["complex_functions"] > 0  # Has functions with complexity > 10
        assert analysis["max_complexity"] > 10

    def test_analyze_code_file_empty(self, complexity_analyzer):
        """Test analyzing empty file."""
        pytest.importorskip("radon")
        analysis = complexity_analyzer.analyze_code_file("", "empty.py")

        assert analysis["total_functions"] == 0
        assert analysis["average_complexity"] == 0.0
        assert analysis["complex_functions"] == 0

    def test_analyze_repository_complexity_with_code(self, complexity_analyzer, repo_with_code):
        """Test repository complexity analysis."""
        pytest.importorskip("radon")
        analysis = complexity_analyzer.analyze_repository_complexity(repo_with_code)

        assert analysis["repository"] == "code-repo"
        assert analysis["has_code_analysis"] is True
        assert analysis["total_files"] == 2
        assert analysis["total_functions"] >= 2
        assert "file_analyses" in analysis
        assert "most_complex_files" in analysis

    def test_analyze_repository_complexity_without_code(
        self, complexity_analyzer, repo_without_code
    ):
        """Test repository analysis without code."""
        analysis = complexity_analyzer.analyze_repository_complexity(repo_without_code)

        assert analysis["repository"] == "no-code"
        assert analysis["has_code_analysis"] is False
        assert analysis["total_files"] == 0
        assert analysis["total_functions"] == 0

    def test_analyze_repository_complexity_no_metadata(self, complexity_analyzer):
        """Test repository with no metadata."""
        repo = Repository(id=3, name="no-meta", full_name="org/no-meta", metadata=None)

        analysis = complexity_analyzer.analyze_repository_complexity(repo)

        assert analysis["has_code_analysis"] is False
        assert analysis["total_files"] == 0

    def test_analyze_repository_complexity_non_python(self, complexity_analyzer):
        """Test repository with non-Python files."""
        repo = Repository(
            id=4,
            name="js-repo",
            full_name="org/js-repo",
            language="JavaScript",
            metadata={"code_files": {"index.js": "console.log('hello');"}},
        )

        analysis = complexity_analyzer.analyze_repository_complexity(repo)

        # Should skip JavaScript files
        assert analysis["has_code_analysis"] is False
        assert analysis["total_files"] == 0

    def test_analyze_repository_complexity_mixed_files(self, complexity_analyzer):
        """Test repository with mixed Python and non-Python files."""
        pytest.importorskip("radon")
        repo = Repository(
            id=5,
            name="mixed-repo",
            full_name="org/mixed",
            language="Python",
            metadata={
                "code_files": {
                    "main.py": "def hello(): return 'world'\n",
                    "config.json": '{"key": "value"}',
                    "README.md": "# Project",
                }
            },
        )

        analysis = complexity_analyzer.analyze_repository_complexity(repo)

        # Should only analyze .py files
        assert analysis["has_code_analysis"] is True
        assert analysis["total_files"] == 1

    def test_analyze_organization_complexity(
        self, complexity_analyzer, repo_with_code, repo_without_code
    ):
        """Test organization-wide complexity analysis."""
        pytest.importorskip("radon")
        repos = [repo_with_code, repo_without_code]

        analysis = complexity_analyzer.analyze_organization_complexity(repos)

        org_metrics = analysis["organization_metrics"]
        assert org_metrics["total_repositories"] == 2
        assert org_metrics["repositories_analyzed"] == 1  # Only one has code
        assert org_metrics["total_files"] > 0
        assert org_metrics["total_functions"] > 0
        assert "repository_analyses" in analysis
        assert "most_complex_repositories" in analysis
        assert "most_maintainable_repositories" in analysis

    def test_analyze_organization_complexity_empty(self, complexity_analyzer):
        """Test organization analysis with no repos."""
        analysis = complexity_analyzer.analyze_organization_complexity([])

        org_metrics = analysis["organization_metrics"]
        assert org_metrics["total_repositories"] == 0
        assert org_metrics["repositories_analyzed"] == 0
        assert org_metrics["total_files"] == 0

    def test_analyze_organization_complexity_no_analyzable_repos(
        self, complexity_analyzer, repo_without_code
    ):
        """Test organization with no analyzable repositories."""
        analysis = complexity_analyzer.analyze_organization_complexity([repo_without_code])

        org_metrics = analysis["organization_metrics"]
        assert org_metrics["total_repositories"] == 1
        assert org_metrics["repositories_analyzed"] == 0
        assert org_metrics["average_complexity"] == 0.0

    def test_save_complexity_report(self, complexity_analyzer, temp_dir):
        """Test saving complexity report to JSON."""
        analysis = {
            "organization_metrics": {
                "total_repositories": 5,
                "total_files": 20,
                "average_complexity": 3.5,
            },
            "repository_analyses": [],
        }

        output_path = temp_dir / "complexity_report.json"
        complexity_analyzer.save_complexity_report(analysis, output_path)

        assert output_path.exists()

        # Verify content
        with open(output_path, encoding="utf-8") as f:
            loaded_data = json.load(f)

        assert loaded_data["organization_metrics"]["total_repositories"] == 5
        assert loaded_data["organization_metrics"]["average_complexity"] == 3.5

    def test_most_complex_files_ordering(self, complexity_analyzer):
        """Test that most complex files are correctly ordered."""
        pytest.importorskip("radon")
        code1 = "def simple(): return 1\n"
        code2 = """
def complex(x):
    if x > 0:
        if x > 10:
            if x > 20:
                return x
    return 0
"""

        repo = Repository(
            id=6,
            name="test-ordering",
            full_name="org/test",
            language="Python",
            metadata={"code_files": {"simple.py": code1, "complex.py": code2}},
        )

        analysis = complexity_analyzer.analyze_repository_complexity(repo)

        # Most complex file should be first
        assert len(analysis["most_complex_files"]) >= 1
        assert analysis["most_complex_files"][0]["filename"] == "complex.py"

    def test_complex_functions_threshold(self, complexity_analyzer):
        """Test that complex functions are correctly counted."""
        pytest.importorskip("radon")
        # Create code with functions of varying complexity
        code = """
def simple1(): return 1

def simple2(): return 2

def complex():
    for i in range(20):
        if i % 2 == 0:
            if i % 3 == 0:
                if i % 5 == 0:
                    if i % 7 == 0:
                        if i % 11 == 0:
                            return i
    return None
"""

        analysis = complexity_analyzer.analyze_code_file(code, "test.py")

        # Should have 3 total functions, at least 1 complex (>10)
        assert analysis["total_functions"] == 3
        assert analysis["complex_functions"] >= 1

    def test_average_complexity_calculation(self, complexity_analyzer, simple_python_code):
        """Test average complexity is calculated correctly."""
        pytest.importorskip("radon")
        analysis = complexity_analyzer.analyze_code_file(simple_python_code, "test.py")

        # Two functions, both with complexity 1
        assert analysis["average_complexity"] == 1.0
        assert analysis["max_complexity"] == 1

    def test_organization_ranking_lists(self, complexity_analyzer):
        """Test that organization rankings are limited to 10 items."""
        pytest.importorskip("radon")
        # Create 15 repos with code
        repos = []
        for i in range(15):
            repos.append(
                Repository(
                    id=i,
                    name=f"repo{i}",
                    full_name=f"org/repo{i}",
                    language="Python",
                    metadata={"code_files": {f"file{i}.py": f"def func{i}(): return {i}\n"}},
                )
            )

        analysis = complexity_analyzer.analyze_organization_complexity(repos)

        # Should be limited to 10
        assert len(analysis["most_complex_repositories"]) <= 10
        assert len(analysis["most_maintainable_repositories"]) <= 10
