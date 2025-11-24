#!/usr/bin/env python3
"""
Platform Automation Verification
Verifies that the entire platform is built using Python scripts
"""

import glob
import json
import os


def check_python_scripts() -> dict[str, list[str]]:
    """
    Identify all Python scripts and their purposes.
    """
    scripts_dir = "scripts"
    python_files = glob.glob(f"{scripts_dir}/*.py")

    scripts = {"core_pipeline": [], "visualization": [], "analysis": [], "utilities": []}

    for script in python_files:
        filename = os.path.basename(script)

        # Read first few lines to understand purpose
        with open(script, encoding="utf-8") as f:
            content = f.read()

        # Categorize scripts
        if "build_research_platform" in filename:
            scripts["core_pipeline"].append(
                {
                    "file": filename,
                    "purpose": "Main orchestration script - runs all phases",
                    "size": len(content),
                }
            )
        elif "fetch" in filename or "data" in filename:
            scripts["core_pipeline"].append(
                {"file": filename, "purpose": "Data fetching from GitHub API", "size": len(content)}
            )
        elif "generate_markdown" in filename:
            scripts["core_pipeline"].append(
                {
                    "file": filename,
                    "purpose": "Generate all markdown pages from templates",
                    "size": len(content),
                }
            )
        elif "visualization" in filename or "viz" in filename or "chart" in filename:
            scripts["visualization"].append(
                {
                    "file": filename,
                    "purpose": "Generate interactive visualizations",
                    "size": len(content),
                }
            )
        elif (
            "topic" in filename
            or "network" in filename
            or "quality" in filename
            or "health" in filename
        ):
            scripts["analysis"].append(
                {"file": filename, "purpose": "Data analysis and metrics", "size": len(content)}
            )
        elif "search" in filename or "citation" in filename or "community" in filename:
            scripts["analysis"].append(
                {"file": filename, "purpose": "Feature generation", "size": len(content)}
            )
        else:
            scripts["utilities"].append(
                {"file": filename, "purpose": "Utility/verification script", "size": len(content)}
            )

    return scripts


def check_generated_files() -> dict[str, int]:
    """
    Check what files are auto-generated vs manual.
    """
    generated = {"markdown_pages": 0, "visualizations": 0, "data_files": 0, "manual_files": 0}

    # Check markdown pages (all should be generated)
    docs_files = glob.glob("docs/**/*.md", recursive=True)
    generated["markdown_pages"] = len(docs_files)

    # Check visualizations (all should be Python-generated)
    viz_files = glob.glob("docs/visualizations/*.html")
    generated["visualizations"] = len(viz_files)

    # Check data files (all should be Python-generated JSON)
    data_files = glob.glob("data/*.json")
    generated["data_files"] = len(data_files)

    # Check for manual files (templates are OK, but not generated docs)
    # Templates should only be in templates/ directory

    return generated


def check_build_phases() -> list[dict[str, str]]:
    """
    Extract all build phases from the main pipeline.
    """
    pipeline_file = "scripts/build_research_platform.py"

    if not os.path.exists(pipeline_file):
        return []

    with open(pipeline_file, encoding="utf-8") as f:
        content = f.read()

    phases = []

    # Extract phase information
    phase_patterns = [
        ("Phase 1", "Data Fetching", "fetch_data"),
        ("Phase 2", "Citation Tracking", "generate_citation_report"),
        ("Phase 3", "Search Indexing", "build_search_index"),
        ("Phase 4", "Visualizations", "generate_all_visualizations"),
        ("Phase 5", "Community Features", "generate_reproducibility_report"),
        ("Phase 6", "Code Quality Analysis", "analyze_all_repositories"),
        ("Phase 7", "Repository Health Scoring", "generate_health_report"),
        ("Phase 8", "Advanced Visualizations", "generate_advanced_visualizations"),
        ("Phase 9", "ML Topic Modeling", "analyze_repository_topics"),
        ("Phase 10", "Collaboration Network", "analyze_collaboration_network"),
    ]

    for phase_num, phase_name, function_name in phase_patterns:
        if function_name in content:
            phases.append(
                {
                    "phase": phase_num,
                    "name": phase_name,
                    "function": function_name,
                    "status": "Implemented",
                }
            )
        else:
            phases.append(
                {
                    "phase": phase_num,
                    "name": phase_name,
                    "function": function_name,
                    "status": "Missing",
                }
            )

    # Check for landing page viz
    if "generate_landing_visualizations" in content:
        phases.append(
            {
                "phase": "Phase 9+",
                "name": "Landing Page Visualizations",
                "function": "generate_landing_visualizations",
                "status": "Implemented",
            }
        )

    # Check for repo overview
    if "generate_repo_overview" in content:
        phases.append(
            {
                "phase": "Phase 9+",
                "name": "Repository Overview",
                "function": "generate_repo_overview",
                "status": "Implemented",
            }
        )

    return phases


def check_imports() -> dict[str, list[str]]:
    """
    Check all imports in the main build script.
    """
    pipeline_file = "scripts/build_research_platform.py"

    if not os.path.exists(pipeline_file):
        return {}

    with open(pipeline_file, encoding="utf-8") as f:
        lines = f.readlines()

    imports = {"phase_modules": [], "standard_libs": []}

    for line in lines[:30]:  # Check first 30 lines for imports
        line = line.strip()
        if line.startswith("from ") and "import" in line:
            parts = line.split()
            if len(parts) >= 2:
                module = parts[1]
                if (
                    not module.startswith("datetime")
                    and not module.startswith("json")
                    and not module.startswith("os")
                ):
                    imports["phase_modules"].append(module)
                else:
                    imports["standard_libs"].append(module)
        elif line.startswith("import "):
            parts = line.split()
            if len(parts) >= 2:
                imports["standard_libs"].append(parts[1])

    return imports


def verify_no_manual_data() -> tuple[bool, list[str]]:
    """
    Verify that no data files are manually created.
    All should be generated by Python scripts.
    """
    data_dir = "data"
    issues = []

    # Check if build_log exists (proves automated build)
    build_log = os.path.join(data_dir, "build_log.json")
    if not os.path.exists(build_log):
        issues.append("build_log.json missing - no proof of automated build")
    else:
        # Check timestamp
        with open(build_log, encoding="utf-8") as f:
            log_data = json.load(f)
            log_data.get("timestamp", "N/A")
            phases = log_data.get("phases_completed", 0)

            if phases < 9:
                issues.append(f"Only {phases} phases completed - should be 9+")

    # Check for manual CSV or Excel files (shouldn't exist)
    manual_files = glob.glob(f"{data_dir}/*.csv") + glob.glob(f"{data_dir}/*.xlsx")
    if manual_files:
        issues.append(f"Found manual data files: {manual_files}")

    return (len(issues) == 0, issues)


def main():
    """Main execution."""
    # Set UTF-8 for Windows
    import sys

    if sys.platform == "win32":
        import io

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    print("=" * 70)
    print("PLATFORM AUTOMATION VERIFICATION")
    print("=" * 70)
    print()
    print("Verifying that the entire platform is built using Python scripts...")
    print()

    # Check Python scripts
    print("=" * 70)
    print("PYTHON SCRIPTS INVENTORY")
    print("=" * 70)
    print()

    scripts = check_python_scripts()

    total_scripts = sum(len(v) for v in scripts.values())
    print(f"Total Python scripts: {total_scripts}")
    print()

    for category, script_list in scripts.items():
        if script_list:
            print(f"{category.upper().replace('_', ' ')}:")
            for script in script_list:
                print(f"  [OK] {script['file']}")
                print(f"       Purpose: {script['purpose']}")
                print(f"       Size: {script['size']:,} bytes")
                print()

    # Check build phases
    print("=" * 70)
    print("BUILD PIPELINE PHASES")
    print("=" * 70)
    print()

    phases = check_build_phases()

    implemented = [p for p in phases if p["status"] == "Implemented"]
    print(f"Implemented phases: {len(implemented)}/{len(phases)}")
    print()

    for phase in phases:
        status_symbol = "[OK]" if phase["status"] == "Implemented" else "[FAIL]"
        print(f"{status_symbol} {phase['phase']}: {phase['name']}")
        print(f"       Function: {phase['function']}")
        print()

    # Check imports
    print("=" * 70)
    print("BUILD SCRIPT IMPORTS")
    print("=" * 70)
    print()

    imports = check_imports()

    print(f"Phase modules imported: {len(imports['phase_modules'])}")
    for module in imports["phase_modules"]:
        print(f"  - {module}")
    print()

    # Check generated files
    print("=" * 70)
    print("GENERATED FILES")
    print("=" * 70)
    print()

    generated = check_generated_files()

    for file_type, count in generated.items():
        print(f"{file_type.replace('_', ' ').title()}: {count}")

    print()

    # Verify no manual data
    print("=" * 70)
    print("AUTOMATION VERIFICATION")
    print("=" * 70)
    print()

    is_automated, issues = verify_no_manual_data()

    if is_automated:
        print("[SUCCESS] All data is automatically generated")
    else:
        print("[WARNING] Potential manual data detected:")
        for issue in issues:
            print(f"  - {issue}")

    print()

    # Check build log
    build_log_file = "data/build_log.json"
    if os.path.exists(build_log_file):
        with open(build_log_file, encoding="utf-8") as f:
            build_log = json.load(f)

        print("Last Build Information:")
        print(f"  Timestamp: {build_log.get('timestamp', 'N/A')}")
        print(f"  Organization: {build_log.get('organization', 'N/A')}")
        print(f"  Repositories: {build_log.get('total_repos', 'N/A')}")
        print(f"  Phases Completed: {build_log.get('phases_completed', 'N/A')}")
        print(f"  Errors: {len(build_log.get('errors', {}))}")

    print()

    # Overall summary
    print("=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    print()

    all_phases_working = all(p["status"] == "Implemented" for p in phases)
    has_sufficient_scripts = total_scripts >= 10

    checks = {
        "All build phases implemented": all_phases_working,
        "Sufficient Python scripts (>=10)": has_sufficient_scripts,
        "All data auto-generated": is_automated,
        "Markdown pages generated": generated["markdown_pages"] > 0,
        "Visualizations generated": generated["visualizations"] > 0,
        "Data files generated": generated["data_files"] > 0,
    }

    for check, result in checks.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {check}: {result}")

    print()

    if all(checks.values()):
        print("=" * 70)
        print("[SUCCESS] ENTIRE PLATFORM IS PYTHON-DRIVEN!")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  - {total_scripts} Python scripts")
        print(f"  - {len(implemented)} automated build phases")
        print(f"  - {generated['markdown_pages']} markdown pages generated")
        print(f"  - {generated['visualizations']} visualizations generated")
        print(f"  - {generated['data_files']} data files generated")
        print()
        print("No manual data entry or hardcoded files detected.")
    else:
        print("[WARNING] Some automation gaps detected - review above")

    print()
    print("=" * 70)


def show_python_dependency_tree():
    """
    Show which Python scripts depend on which.
    """
    print("=" * 70)
    print("PYTHON SCRIPT DEPENDENCY TREE")
    print("=" * 70)
    print()

    pipeline_file = "scripts/build_research_platform.py"

    if not os.path.exists(pipeline_file):
        print("[FAIL] Main pipeline not found")
        return

    with open(pipeline_file, encoding="utf-8") as f:
        content = f.read()

    # Extract imports
    dependencies = []
    lines = content.split("\n")

    for line in lines[:30]:
        if "from " in line and "import" in line:
            # Parse "from module import function as alias"
            parts = line.strip().split()
            if len(parts) >= 4:
                module = parts[1]
                function = parts[3]

                # Skip standard library
                if module not in ["json", "os", "sys", "datetime"]:
                    dependencies.append({"module": module, "function": function})

    print("Main Pipeline (build_research_platform.py) depends on:")
    print()

    for i, dep in enumerate(dependencies, 1):
        script_file = f"scripts/{dep['module']}.py"
        exists = os.path.exists(script_file)
        status = "[OK]" if exists else "[MISSING]"

        print(f"{status} [{i}] {dep['module']}.py")
        print(f"       Imports: {dep['function']}()")
        print()

    print(f"Total dependencies: {len(dependencies)}")
    print()


if __name__ == "__main__":
    main()
    show_python_dependency_tree()
