#!/usr/bin/env python3
"""
Master orchestration script for building the complete research platform.
Runs all phases: data fetching, parsing, visualization, search indexing, etc.
"""

import json
import os
import sys
from datetime import datetime

# Import all phase modules
from fetch_org_data_research import main as fetch_data
from citation_tracker import generate_citation_report
from search_indexer import build_search_index
from visualization_builder import generate_all_visualizations
from community_features import generate_reproducibility_report
from advanced_visualizations import generate_advanced_visualizations
from code_quality_analyzer import analyze_all_repositories
from repository_health_scorer import generate_health_report
from ml_topic_modeling import analyze_repository_topics
from collaboration_network_analyzer import analyze_collaboration_network
from create_landing_page_viz import generate_landing_visualizations
from create_repo_overview import main as generate_repo_overview


class ResearchPlatformBuilder:
    """Orchestrate building of complete research platform."""

    def __init__(self, org_name: str, github_token: str):
        self.org_name = org_name
        self.github_token = github_token
        self.build_log = []

    def log(self, message: str):
        """Log a build message."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.build_log.append(log_message)

    def run_phase(self, phase_name: str, phase_func, *args, **kwargs):
        """Run a build phase with error handling."""
        self.log(f"=" * 60)
        self.log(f"Starting {phase_name}")
        self.log(f"=" * 60)

        try:
            result = phase_func(*args, **kwargs)
            self.log(f"{phase_name} completed successfully")
            return result, None
        except Exception as e:
            error_msg = f"ERROR in {phase_name}: {str(e)}"
            self.log(error_msg)
            return None, str(e)

    def build_platform(self, skip_phases: list = None):
        """
        Build complete research platform.

        Args:
            skip_phases: List of phase names to skip
        """
        skip_phases = skip_phases or []
        results = {}
        errors = {}

        self.log("=" * 60)
        self.log("RESEARCH PLATFORM BUILD STARTED")
        self.log(f"Organization: {self.org_name}")
        self.log("=" * 60)

        # Set environment variables
        os.environ['GITHUB_TOKEN'] = self.github_token
        os.environ['GITHUB_ORG'] = self.org_name

        # Phase 1: Fetch data with research metadata
        if 'fetch_data' not in skip_phases:
            result, error = self.run_phase(
                "Phase 1: Data Fetching",
                fetch_data
            )
            if error:
                errors['fetch_data'] = error
                self.log("CRITICAL: Data fetch failed. Cannot continue.")
                return {'errors': errors, 'log': self.build_log}

        # Load repos data for subsequent phases
        try:
            with open('data/repos.json', 'r', encoding='utf-8') as f:
                repos_data = json.load(f)
            self.log(f"Loaded {len(repos_data)} repositories")
        except Exception as e:
            self.log(f"ERROR: Could not load repos data: {e}")
            return {'errors': {'load_data': str(e)}, 'log': self.build_log}

        # Phase 2: Citation tracking
        if 'citations' not in skip_phases:
            result, error = self.run_phase(
                "Phase 2: Citation Tracking",
                generate_citation_report,
                repos_data
            )
            if error:
                errors['citations'] = error
            else:
                results['citation_report'] = result

        # Load citation report if available
        citation_report = None
        if os.path.exists('data/citation_report.json'):
            try:
                with open('data/citation_report.json', 'r', encoding='utf-8') as f:
                    citation_report = json.load(f)
            except:
                pass

        # Phase 3: Search indexing
        if 'search' not in skip_phases:
            result, error = self.run_phase(
                "Phase 3: Search Indexing",
                build_search_index,
                repos_data
            )
            if error:
                errors['search'] = error
            else:
                results['search_index'] = result

        # Phase 4: Visualizations
        if 'visualizations' not in skip_phases:
            result, error = self.run_phase(
                "Phase 4: Visualizations",
                generate_all_visualizations,
                repos_data,
                citation_report
            )
            if error:
                errors['visualizations'] = error
            else:
                results['visualizations'] = result

        # Phase 5: Community features & reproducibility
        if 'community' not in skip_phases:
            result, error = self.run_phase(
                "Phase 5: Community Features",
                generate_reproducibility_report,
                repos_data
            )
            if error:
                errors['community'] = error
            else:
                results['reproducibility_report'] = result

        # Load reproducibility report for subsequent phases
        reproducibility_report = None
        if os.path.exists('data/reproducibility_report.json'):
            try:
                with open('data/reproducibility_report.json', 'r', encoding='utf-8') as f:
                    reproducibility_report = json.load(f)
            except:
                pass

        # Phase 6: Code quality analysis
        if 'code_quality' not in skip_phases:
            result, error = self.run_phase(
                "Phase 6: Code Quality Analysis",
                analyze_all_repositories,
                repos_data
            )
            if error:
                errors['code_quality'] = error
            else:
                results['code_quality'] = result

        # Load code quality report for health scoring
        code_quality_report = None
        if os.path.exists('data/code_quality_report.json'):
            try:
                with open('data/code_quality_report.json', 'r', encoding='utf-8') as f:
                    code_quality_report = json.load(f)
            except:
                pass

        # Phase 7: Repository health scoring
        if 'health' not in skip_phases:
            result, error = self.run_phase(
                "Phase 7: Repository Health Scoring",
                generate_health_report,
                repos_data,
                code_quality_report
            )
            if error:
                errors['health'] = error
            else:
                results['health_report'] = result

        # Phase 8: Advanced visualizations
        if 'advanced_viz' not in skip_phases:
            result, error = self.run_phase(
                "Phase 8: Advanced Visualizations",
                generate_advanced_visualizations,
                repos_data,
                citation_report,
                reproducibility_report
            )
            if error:
                errors['advanced_viz'] = error
            else:
                results['advanced_visualizations'] = result

        # Phase 9: ML Topic Modeling
        if 'ml_topics' not in skip_phases:
            result, error = self.run_phase(
                "Phase 9: ML Topic Modeling",
                analyze_repository_topics,
                repos_data,
                'both'  # Use both NMF and LDA
            )
            if error:
                errors['ml_topics'] = error
            else:
                results['ml_topics'] = result

                # Generate landing page visualizations from topic analysis
                self.log("Generating landing page topic visualizations...")
                try:
                    landing_viz = generate_landing_visualizations()
                    results['landing_viz'] = landing_viz
                    self.log(f"Generated {len(landing_viz)} landing page visualizations")
                except Exception as e:
                    self.log(f"Warning: Could not generate landing visualizations: {e}")

                # Generate repository overview
                self.log("Generating interactive repository overview...")
                try:
                    repo_overview = generate_repo_overview()
                    results['repo_overview'] = repo_overview
                    self.log(f"Generated repository overview visualizations")
                except Exception as e:
                    self.log(f"Warning: Could not generate repository overview: {e}")

        # Phase 10: Collaboration Network Analysis
        if 'collab_network' not in skip_phases:
            result, error = self.run_phase(
                "Phase 10: Collaboration Network Analysis",
                analyze_collaboration_network,
                repos_data,
                self.org_name,
                self.github_token
            )
            if error:
                errors['collab_network'] = error
            else:
                results['collaboration_network'] = result

        # Save build log
        self.log("=" * 60)
        self.log("BUILD COMPLETED")
        self.log(f"Errors: {len(errors)}")
        self.log("=" * 60)

        build_summary = {
            'timestamp': datetime.now().isoformat(),
            'organization': self.org_name,
            'total_repos': len(repos_data),
            'phases_completed': len(results),
            'errors': errors,
            'log': self.build_log
        }

        with open('data/build_log.json', 'w', encoding='utf-8') as f:
            json.dump(build_summary, f, indent=2, ensure_ascii=False)

        return build_summary


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Build complete research platform from GitHub organization'
    )
    parser.add_argument(
        'org_name',
        nargs='?',
        help='GitHub organization name'
    )
    parser.add_argument(
        '--skip',
        nargs='+',
        choices=['fetch_data', 'citations', 'search', 'visualizations', 'community',
                'code_quality', 'health', 'advanced_viz', 'ml_topics', 'collab_network'],
        help='Phases to skip'
    )
    parser.add_argument(
        '--token',
        help='GitHub personal access token (or set GITHUB_TOKEN env var)'
    )

    args = parser.parse_args()

    # Get organization name
    org_name = args.org_name or os.environ.get('GITHUB_ORG')
    if not org_name:
        print("ERROR: Organization name not provided")
        print("Usage: python build_research_platform.py ORG_NAME")
        print("   or: export GITHUB_ORG='org_name'")
        sys.exit(1)

    # Get GitHub token
    github_token = args.token or os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("ERROR: GitHub token not provided")
        print("Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)

    # Build platform
    builder = ResearchPlatformBuilder(org_name, github_token)
    summary = builder.build_platform(skip_phases=args.skip or [])

    # Print summary
    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)
    print(f"Organization: {summary['organization']}")
    print(f"Total repositories: {summary['total_repos']}")
    print(f"Phases completed: {summary['phases_completed']}")
    print(f"Errors: {len(summary['errors'])}")

    if summary['errors']:
        print("\nErrors encountered:")
        for phase, error in summary['errors'].items():
            print(f"  - {phase}: {error[:100]}")

    print(f"\nBuild log saved to: data/build_log.json")

    # Exit with error code if there were errors
    sys.exit(1 if summary['errors'] else 0)


if __name__ == '__main__':
    main()
