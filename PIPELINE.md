# Automated Pipeline Documentation

## Overview

The entire research platform is built and maintained using **Python automation**. No manual data entry or file creation required.

## Pipeline Architecture

### Automated Rebuild Schedule

The platform automatically rebuilds:
- **Daily at 2 AM UTC** (via GitHub Actions)
- **On script updates** (when scripts/ files change)
- **Manual trigger** (via GitHub Actions UI or local script)

## Quick Start

### Local Rebuild (Manual)

```bash
# Set environment variables
export GITHUB_TOKEN='your_token_here'
export GITHUB_ORG='Digital-AI-Finance'

# Run complete rebuild
python rebuild.py
```

Or run individual components:

```bash
# Full 10-phase build
python scripts/build_research_platform.py Digital-AI-Finance

# Generate markdown pages
python scripts/generate_markdown.py

# Verify automation
python scripts/verify_platform_automation.py
```

### GitHub Actions (Automated)

The workflow runs automatically. To trigger manually:

1. Go to: https://github.com/Digital-AI-Finance/org-dashboard/actions
2. Select "Rebuild Research Platform"
3. Click "Run workflow"

## Build Phases

The build pipeline consists of 12 automated phases:

| Phase | Script | Output |
|-------|--------|--------|
| 1 | `fetch_org_data_research.py` | `data/repos.json` |
| 2 | `citation_tracker.py` | `data/citation_report.json` |
| 3 | `search_indexer.py` | `data/search_index.pkl` |
| 4 | `visualization_builder.py` | 5 base visualizations |
| 5 | `community_features.py` | `data/reproducibility_report.json` |
| 6 | `code_quality_analyzer.py` | `data/code_quality_report.json` |
| 7 | `repository_health_scorer.py` | `data/repository_health_report.json` |
| 8 | `advanced_visualizations.py` | 6 advanced visualizations |
| 9 | `ml_topic_modeling.py` | `data/ml_topic_analysis.json` + topic viz |
| 9+ | `create_landing_page_viz.py` | 4 landing page visualizations |
| 9+ | `create_repo_overview.py` | Repository gallery + network |
| 10 | `collaboration_network_analyzer.py` | Network visualizations |

**Final Step**: `generate_markdown.py` renders all Jinja2 templates to markdown

## Generated Assets

### Data Files (11)
- `repos.json` - All repository metadata
- `citation_report.json` - Citation tracking
- `citation_history.json` - Citation timeline
- `search_index.pkl` - Full-text search index
- `reproducibility_report.json` - Reproducibility scores
- `code_quality_report.json` - Code quality metrics
- `repository_health_report.json` - Health scores
- `ml_topic_analysis.json` - ML topic modeling results
- `collaboration_network.json` - Collaboration graph
- `build_log.json` - Build execution log

### Markdown Pages (56)
- `index.md` - Main landing page
- `stats.md` - Statistics overview
- `repos/*.md` - Individual repository pages (6)
- `by-language/*.md` - Language-filtered pages (4)
- `by-topic/*.md` - Topic-filtered pages (10+)

### Visualizations (22)
- `topic_distribution_*.html` - Topic analysis charts (4)
- `topic_words_*.html` - Topic word clouds (4)
- `landing_topic_bubbles*.html` - 3D topic bubbles (4)
- `activity_heatmap.html` - Repository activity
- `topic_sunburst.html` - Hierarchical topics
- `reproducibility_radar.html` - Multi-dimensional scoring
- `repository_treemap.html` - Repository size/stars
- `metric_comparison.html` - Parallel coordinates
- `code_structure_scores.html` - Code quality
- `repository_health_scores.html` - Health metrics
- `repository_overview.html` - **Interactive gallery**
- `repository_network.html` - **Topic network graph**
- `collaboration_network.html` - Collaboration graph

## GitHub Actions Workflow

### Workflow File
`.github/workflows/rebuild-platform.yml`

### What It Does
1. Checks out repository
2. Sets up Python 3.12
3. Installs all dependencies
4. Runs complete build pipeline
5. Generates markdown pages
6. Commits changes (if any)
7. Pushes to main branch
8. GitHub Pages auto-deploys

### Monitoring

View workflow runs:
https://github.com/Digital-AI-Finance/org-dashboard/actions

### Manual Trigger

Via GitHub UI:
1. Actions tab
2. "Rebuild Research Platform" workflow
3. "Run workflow" button

Via CLI:
```bash
gh workflow run rebuild-platform.yml
```

## Verification Scripts

### Check All Links
```bash
python scripts/check_links.py
```
Verifies:
- All repository URLs are accessible
- Filter buttons work
- JavaScript handlers present
- Interactive elements functional

### Verify Automation
```bash
python scripts/verify_platform_automation.py
```
Confirms:
- All Python scripts present
- All build phases implemented
- No manual data files
- Complete automation

## Environment Variables

Required for full functionality:

```bash
GITHUB_TOKEN=ghp_your_token_here    # GitHub API access
GITHUB_ORG=Digital-AI-Finance        # Organization name
```

## Dependencies

Install all dependencies:

```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install PyGithub requests Jinja2 plotly scikit-learn networkx beautifulsoup4
```

## Troubleshooting

### Rate Limits
If you hit GitHub API rate limits:
- Ensure `GITHUB_TOKEN` is set
- Wait for rate limit reset
- Use `--skip` flag to skip phases

### Partial Rebuild
Skip specific phases:
```bash
python scripts/build_research_platform.py Digital-AI-Finance --skip visualizations ml_topics
```

### Force Rebuild
Delete data files and rebuild:
```bash
rm -rf data/*.json
python rebuild.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions (Scheduled/Manual Trigger)              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  build_research_platform.py (Main Orchestrator)         │
├─────────────────────────────────────────────────────────┤
│  Phase 1:  fetch_org_data_research.py                   │
│  Phase 2:  citation_tracker.py                          │
│  Phase 3:  search_indexer.py                            │
│  Phase 4:  visualization_builder.py                     │
│  Phase 5:  community_features.py                        │
│  Phase 6:  code_quality_analyzer.py                     │
│  Phase 7:  repository_health_scorer.py                  │
│  Phase 8:  advanced_visualizations.py                   │
│  Phase 9:  ml_topic_modeling.py                         │
│           ├─ create_landing_page_viz.py                 │
│           └─ create_repo_overview.py                    │
│  Phase 10: collaboration_network_analyzer.py            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  generate_markdown.py (Jinja2 Templating)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  docs/ (Generated Static Site)                          │
│  ├─ index.md                                            │
│  ├─ repos/*.md                                          │
│  ├─ by-language/*.md                                    │
│  ├─ by-topic/*.md                                       │
│  └─ visualizations/*.html                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  GitHub Pages Deployment (Automatic)                    │
│  https://digital-ai-finance.github.io/org-dashboard/    │
└─────────────────────────────────────────────────────────┘
```

## Outputs

- **Live Site**: https://digital-ai-finance.github.io/org-dashboard/
- **Repository Gallery**: https://digital-ai-finance.github.io/org-dashboard/visualizations/repository_overview.html
- **Build Logs**: `data/build_log.json`
- **All Visualizations**: `docs/visualizations/*.html`

## Performance

- **Build Time**: ~30-60 seconds (depends on repo count)
- **22 Python Scripts**: 100% automated
- **56+ Pages Generated**: Zero manual editing
- **22 Visualizations**: All Plotly-based
- **GitHub API Calls**: ~10-15 per repository
