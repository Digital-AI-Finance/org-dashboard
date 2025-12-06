# org-dashboard

Automated dashboard for monitoring all repositories in the Digital-AI-Finance organization

[View on GitHub](https://github.com/Digital-AI-Finance/org-dashboard){ .md-button .md-button--primary }
[Homepage](https://digital-ai-finance.github.io/org-dashboard){ .md-button }

---





## Information

| Property | Value |
|----------|-------|
| Language | Python |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-11-21 |
| Last Updated | 2025-12-05 |
| Last Push | 2025-12-05 |
| Contributors | 2 |
| Default Branch | main |
| Visibility | public |






## Datasets

This repository includes 20 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [coverage.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/coverage.json) | .json | 59.32 KB |

| [data](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data) |  | 0.0 KB |

| [build_log.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/build_log.json) | .json | 4.05 KB |

| [citation_history.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/citation_history.json) | .json | 53.31 KB |

| [citation_report.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/citation_report.json) | .json | 3.72 KB |

| [code_quality_report.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/code_quality_report.json) | .json | 16.79 KB |

| [collaboration_network.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/collaboration_network.json) | .json | 6.0 KB |

| [ml_topic_analysis.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/ml_topic_analysis.json) | .json | 29.22 KB |

| [repos.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/repos.json) | .json | 268.43 KB |

| [repository_health_report.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/repository_health_report.json) | .json | 51.26 KB |

| [reproducibility_report.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/reproducibility_report.json) | .json | 30.38 KB |

| [research_metadata.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/research_metadata.json) | .json | 95.57 KB |

| [search_index.pkl](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/search_index.pkl) | .pkl | 222.63 KB |

| [stats.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/data/stats.json) | .json | 2.91 KB |

| [data](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/docs/data) |  | 0.0 KB |

| [search_data.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/docs/data/search_data.json) | .json | 642.52 KB |

| [search_data_minimal.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/docs/data/search_data_minimal.json) | .json | 457.84 KB |

| [citation_network.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/docs/visualizations/citation_network.json) | .json | 0.33 KB |

| [collaboration_network.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/docs/visualizations/collaboration_network.json) | .json | 1.42 KB |

| [research_metadata_schema.json](https://github.com/Digital-AI-Finance/org-dashboard/blob/main/schemas/research_metadata_schema.json) | .json | 5.45 KB |




## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Enabled

## README

# GitHub Organization Research Platform

A comprehensive, automated research platform for academic GitHub organizations. Combines repository monitoring with advanced research features including publication tracking, citation analysis, reproducibility scoring, and community verification.

Live Demo: https://digital-ai-finance.github.io/org-dashboard/

## Core Features

- Automatic daily updates via GitHub Actions
- Beautiful, searchable documentation site
- Repository catalog with detailed information
- Statistics and analytics
- Organization by language and topics
- Mobile-responsive design
- Zero server costs (runs entirely on GitHub)

## Research Platform Features

### Publication Tracking
- Automatic extraction of DOIs, arXiv IDs, SSRN papers from READMEs
- Academic database integration (CrossRef, arXiv)
- Publication metadata enrichment
- Citation count tracking

### Code & Data
- Jupyter notebook rendering
- Dataset detection and cataloging
- Dependency analysis
- Code language statistics

### Reproducibility
- Automated reproducibility scoring (100-point scale)
- Badge system (Gold/Silver/Bronze)
- Environment configuration detection
- Docker support tracking

### Community Features
- Replication attempt tracking
- Community verification system
- Peer review ratings
- Success rate metrics

### Advanced Search
- Full-text search across all repositories
- Faceted navigation
- TF-IDF relevance scoring
- Autocomplete suggestions

### Visualizations
- Interactive Plotly charts
- Citation network graphs
- Publication timelines
- Language distribution
- Collaboration networks

## Architecture

- **Data Fetching**: Python script using PyGithub to fetch org data + research metadata extraction
- **Academic APIs**: CrossRef, arXiv integration for publication enrichment
- **Analysis**: Citation tracking, reproducibility scoring, search indexing
- **Markdown Generation**: Jinja2 templates for dynamic content
- **Visualizations**: Interactive Plotly charts, network graphs
- **Static Site**: MkDocs Material theme
- **Automation**: GitHub Actions for scheduled updates
- **Hosting**: GitHub Pages (free)

## Live Demo

Visit our live demo at: https://digital-ai-finance.github.io/org-dashboard/

The demo includes 4 example repositories showcasing different research features:

1. **org-dashboard** - This repository (meta!)
2. **portfolio-optimization-ml** - ML research with arXiv papers and DOIs
3. **credit-risk-prediction** - Neural networks with SSRN publications and notebooks
4. **market-microstructure** - HFT research with Zenodo datasets and Docker

Features demonstrated:
- Publications with DOI/arXiv links and citation counts
- Reproducibility scores and badges
- Community replication attempts and reviews
- Dataset cataloging
- Interactive visualizations

## Setup Instructions

### 1. Create GitHub Personal Access Token

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Org Dashboard")
4. Select scopes:
   - `repo` (Full control of private repositories)
   - `read:org` (Read org and team membership)
5. Click "Generate token"
6. Copy the token immediately (you will not see it again)

### 2. Fork or Create This Repository

1. Create a new repository in your GitHub organization
2. Clone this repository or copy all files to your new repo
3. Push to GitHub

### 3. Configure Repository Secrets

1. Go to your repository Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `GH_PAT`: Your GitHub Personal Access Token
   - `ORG_NAME`: Your organization name (e.g., "my-org")

### 4. Enable GitHub Pages

1. Go to repository Settings > Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`
4. Save

### 5. Run Initial Workflow

1. Go to Actions tab
2. Select "Update Dashboard" workflow
3. Click "Run workflow"
4. Wait for completion (2-5 minutes)

### 6. Access Your Dashboard

Your dashboard will be available at:
`https://YOUR_ORG.github.io/REPO_NAME/`

## Configuration

### Update Frequency

Edit `.github/workflows/update-dashboard.yml` to change schedule:

```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * 0'  # Weekly on Sunday
```

### Customize Appearance

Edit `mkdocs.yml` to change:
- Site name and description
- Theme colors
- Navigation structure
- Enabled features

### Customize Templates

Edit files in `templates/` directory to change:
- Page layouts
- Content structure
- Displayed information

## Local Development

### Prerequisites

- Python 3.11+
- Git

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Fetch Data Locally

```bash
export GITHUB_TOKEN='your_token_here'
export GITHUB_ORG='your_org_name'
python scripts/fetch_org_data.py
```

Or with arguments:

```bash
export GITHUB_TOKEN='your_token_here'
python scripts/fetch_org_data.py your_org_name
```

### Generate Markdown

```bash
python scripts/generate_markdown.py
```

### Preview Site Locally

```bash
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.

### Build Static Site

```bash
mkdocs build
```

Output will be in `site/` directory.

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── update-dashboard.yml  # GitHub Actions workflow
├── scripts/
│   ├── fetch_org_data.py        # Fetch data from GitHub API
│   └── generate_markdown.py     # Generate markdown from data
├── templates/                   # Jinja2 templates
│   ├── index.md.j2
│   ├── stats.md.j2
│   ├── repo.md.j2
│   └── ...
├── docs/                        # Generated markdown (committed)
│   ├── index.md
│   ├── stats.md
│   ├── repos/
│   ├── by-language/
│   └── by-topic/
├── data/                        # Generated JSON data (committed)
│   ├── repos.json
│   └── stats.json
├── mkdocs.yml                   # MkDocs configuration
├── requirements.txt             # Python dependencies
└── README.md
```

## Troubleshooting

### Workflow Fails with Authentication Error

- Verify `GH_PAT` secret is set correctly
- Ensure token has required scopes (`repo`, `read:org`)
- Token may have expired - regenerate and update secret

### No Changes Detected

- Check if organization has any repositories
- Verify `ORG_NAME` secret is correct
- Check workflow logs for errors

### Pages Not Deploying

- Ensure GitHub Pages is enabled in repository settings
- Check that `gh-pages` branch exists
- Verify workflow has `contents: write` permission

### Rate Limiting

- GitHub API has rate limits (5000 requests/hour for authenticated requests)
- For large organizations, consider caching or reducing update frequency
- Workflow implements basic rate limit handling

### Local Development Issues

**Module not found:**
```bash
pip install -r requirements.txt
```

**Permission denied:**
```bash
chmod +x scripts/*.py
```

**Data files missing:**
Run fetch script first before generating markdown.

## Customization Ideas

- Add CI/CD status badges
- Include code quality metrics
- Show dependency vulnerabilities
- Add commit activity graphs
- Display contributor statistics
- Track issue response times
- Monitor PR merge times

## GitHub Actions Free Tier Limits

- 2000 minutes/month for free accounts
- This workflow uses ~2-5 minutes per run
- Daily runs: ~150 minutes/month
- Well within free tier limits

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this for your organization.

## Credits

Built with:
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Jinja2](https://jinja.palletsprojects.com/)
