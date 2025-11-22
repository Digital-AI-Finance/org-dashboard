#!/usr/bin/env python3
"""
Quick Rebuild Script
Runs the complete platform rebuild pipeline
"""

import os
import subprocess
import sys
from datetime import datetime


def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Main execution."""
    print("=" * 70)
    print("PLATFORM REBUILD SCRIPT")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check environment
    org_name = os.environ.get("GITHUB_ORG", "Digital-AI-Finance")
    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        print("WARNING: GITHUB_TOKEN not set in environment")
        print("Limited API rate limits will apply")
        print()

    print(f"Organization: {org_name}")
    print()

    # Step 1: Run main build
    success = run_command(
        f"python scripts/build_research_platform.py {org_name}",
        "Step 1: Running complete platform build (10 phases)",
    )

    if not success:
        print("\n[FAIL] Build failed")
        sys.exit(1)

    # Step 2: Generate markdown
    success = run_command(
        "python scripts/generate_markdown.py", "Step 2: Generating all markdown pages"
    )

    if not success:
        print("\n[FAIL] Markdown generation failed")
        sys.exit(1)

    # Step 3: Verify automation
    print(f"\n{'='*70}")
    print("Step 3: Verifying automation")
    print(f"{'='*70}")

    run_command("python scripts/verify_platform_automation.py", "Running verification")

    # Summary
    print("\n" + "=" * 70)
    print("REBUILD COMPLETE")
    print("=" * 70)
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Next steps:")
    print("  1. Review generated files in docs/")
    print("  2. Test visualizations locally")
    print("  3. Deploy to GitHub Pages:")
    print("     git add docs/ data/")
    print("     git commit -m 'Update dashboard data'")
    print("     git push origin main")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
