#!/usr/bin/env python3
"""
Compatibility wrapper for running the platform.
Can use either old scripts or new architecture based on feature flag.
"""

import os
import sys


def main():
    """Main entry point with feature flag support."""
    use_new_architecture = os.environ.get("USE_NEW_ARCH", "false").lower() == "true"

    if use_new_architecture:
        print("Running with NEW architecture (async, modular)")
        print("=" * 70)
        from src.research_platform.__main__ import main as new_main

        return new_main()
    else:
        print("Running with LEGACY architecture (scripts)")
        print("=" * 70)
        # Run the original rebuild script
        import subprocess

        result = subprocess.run(
            [sys.executable, "rebuild.py"],
            env=os.environ.copy(),
        )
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
