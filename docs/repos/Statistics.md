# Statistics



[View on GitHub](https://github.com/Digital-AI-Finance/Statistics){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | TeX |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-11-30 |
| Last Updated | 2025-11-30 |
| Last Push | 2025-11-30 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | private |






## Datasets

This repository includes 15 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [data](https://github.com/Digital-AI-Finance/Statistics/blob/main/data) |  | 0.0 KB |

| [.gitkeep](https://github.com/Digital-AI-Finance/Statistics/blob/main/data/.gitkeep) |  | 0.1 KB |

| [datasets](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets) |  | 0.0 KB |

| [README.md](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/README.md) | .md | 3.59 KB |

| [agricultural_experiment.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/agricultural_experiment.csv) | .csv | 3.81 KB |

| [clinical_trial.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/clinical_trial.csv) | .csv | 2.18 KB |

| [drug_dosage_study.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/drug_dosage_study.csv) | .csv | 3.42 KB |

| [education_intervention.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/education_intervention.csv) | .csv | 0.6 KB |

| [employee_satisfaction.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/employee_satisfaction.csv) | .csv | 3.41 KB |

| [environmental_study.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/environmental_study.csv) | .csv | 6.36 KB |

| [manufacturing_quality.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/manufacturing_quality.csv) | .csv | 0.64 KB |

| [marketing_campaigns.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/marketing_campaigns.csv) | .csv | 4.03 KB |

| [medical_treatment.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/medical_treatment.csv) | .csv | 2.32 KB |

| [reaction_time_study.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/reaction_time_study.csv) | .csv | 2.99 KB |

| [website_testing.csv](https://github.com/Digital-AI-Finance/Statistics/blob/main/lesson2_hypothesis/datasets/website_testing.csv) | .csv | 71.91 KB |




## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# GitHub Organization Dashboard

Automated interactive dashboard for monitoring repository statistics in the Digital-AI-Finance organization. Features real-time data visualization with daily updates via GitHub Actions.

## Features

- **Automated Data Collection**: Daily updates via GitHub Actions
- **Interactive Visualizations**: Powered by Plotly for rich, interactive charts
- **Comprehensive Metrics**:
  - Repository activity timeline
  - Commit patterns and trends
  - Language distribution analysis
  - Repository maturity scoring
  - Research focus areas
  - Contributor analytics
- **Modern UI**: Dark theme with GitHub-inspired design
- **Zero Maintenance**: Fully automated pipeline with scheduled updates
- **GitHub Pages Deployment**: Accessible via web browser

## Quick Start

### Local Development

1. **Clone the repository**
   ```powershell
   git clone https://github.com/Digital-AI-Finance/dashboard.git
   cd dashboard
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up GitHub token** (optional but recommended)
   ```powershell
   # Windows PowerShell
   $env:GITHUB_TOKEN="your_github_personal_access_token"

   # Or create a .env file
   echo "GITHUB_TOKEN=your_token_here" > .env
   ```

4. **Run the dashboard update**
   ```powershell
   python run_update.py
   ```

5. **View the dashboard**
   Open `index.html` in your browser

### GitHub Token Setup

For higher API rate limits (5000 requests/hour vs 60), create a GitHub Personal Access Token:

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `public_repo`, `read:org`
4. Copy the token
5. Set as environment variable `GITHUB_TOKEN`

## Configuration

Edit `config.yml` to customize:

```yaml
# Organization to monitor
organization: "Digital-AI-Finance"

# Dashboard settings
dashboard:
  title: "Your Custom Title"
  update_frequency: "daily"

# Visualization toggles
charts:
  repository_activity:
    enabled: true
    days_history: 90  # Adjust time window

  technology_stack:
    enabled: true

  research_impact:
    enabled: true

  repository_maturity:
    enabled: true

# Color scheme
colors:
  background: "#0d1117"
  primary: "#58a6ff"
  # ... customize colors
```

## GitHub Actions Automation

The dashboard automatically updates daily via GitHub Actions:

### Setup

1. **Enable GitHub Pages**
   - Go to repository Settings > Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` / root

2. **Verify workflow permissions**
   - Go to Settings > Actions > General
   - Workflow permissions: Read and write permissions
   - Save

3. **Manual trigger** (optional)
   - Go to Actions tab
   - Select "Update Dashboard" workflow
   - Click "Run workflow"

### Schedule

- **Automatic**: Daily at midnight UTC
- **On push**: When code changes are pushed
- **Manual**: Via Actions tab

## Project Structure

```
github-dashboard/
|-- .github/
|   `-- workflows/
|       `-- update-dashboard.yml    # GitHub Actions workflow
|
|-- data/
|   |-- repository_stats.json       # Fetched GitHub data (generated)
|   `-- cache/                      # API response cache (generated)
|
|-- fetch_github_data.py            # GitHub API data fetcher
|-- generate_dashboard.py           # Dashboard HTML generator
|-- run_update.py                   # Convenience script to run both
|
|-- config.yml                      # Configuration file
|-- requirements.txt                # Python dependencies
|-- .gitignore                      # Git ignore rules
|
|-- index.html                      # Generated dashboard (output)
`-- README.md                       # This file
```

## Scripts Overview

### fetch_github_data.py

Fetches comprehensive data from GitHub API:
- Organization metadata
- Repository details (commits, languages, contributors)
- Activity metrics
- Maturity scoring
- Rate limit management

**Usage:**
```powershell
python fetch_github_data.py
```

### generate_dashboard.py

Generates interactive HTML dashboard with Plotly charts:
- Commit timeline
- Language distribution
- Repository statistics
- Maturity gauges
- Research focus areas
- Contributor activity

**Usage:**
```powershell
python generate_dashboard.py
```

### run_update.py

Runs complete update pipeline (fetch + generate):

**Usage:**
```powershell
python run_update.py
```

## Visualizations

### 1. Commit Activity Timeline
Line chart showing commit activity across all repositories over the last 90 days.

### 2. Technology Stack Distribution
Pie chart displaying programming language usage across the organization.

### 3. Repository Statistics
Bar charts comparing commits, stars, and forks across repositories.

### 4. Repository Maturity Scores
Gauge charts showing maturity levels based on:
- Commit activity (20%)
- Documentation (20%)
- Testing infrastructure (20%)
- License presence (15%)
- CI/CD setup (15%)
- Community engagement (10%)

**Maturity Stages:**
- Production: 80-100%
- Beta: 60-79%
- Alpha: 40-59%
- Planning: 20-39%
- Concept: 0-19%

### 5. Research Focus Areas
Bar chart of research topics extracted from repository descriptions.

### 6. Contributor Activity
Bar chart showing contributor counts per repository.

## Customization

### Modify Charts

Edit `generate_dashboard.py` to customize visualizations:

```python
def create_custom_chart(self, data: Dict) -> str:
    # Your custom Plotly chart code
    fig = go.Figure(...)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
```

Add to `generate_html()` method:
```python
custom_chart = self.create_custom_chart(data)
```

Update HTML template to include:
```html
<div class="chart-section">
    <h2>Custom Chart Title</h2>
    {{ custom_chart|safe }}
</div>
```

### Change Color Scheme

Edit `config.yml` colors section:

```yaml
colors:
  background: "#your_color"
  primary: "#your_color"
  # ... etc
```

### Adjust Data Collection

Modify `fetch_github_data.py`:
- Change `since_days` parameter for longer/shorter history
- Add additional API endpoints
- Customize maturity scoring weights

## Troubleshooting

### Rate Limit Errors

**Problem**: API rate limit exceeded

**Solution**:
- Set `GITHUB_TOKEN` environment variable
- Reduce update frequency
- Enable caching in config.yml

### Missing Data

**Problem**: Charts show no data

**Solution**:
- Verify `data/repository_stats.json` exists
- Check GitHub token permissions
- Run `python fetch_github_data.py` manually to see errors

### GitHub Pages Not Updating

**Problem**: Dashboard not showing latest data

**Solution**:
- Check Actions tab for workflow errors
- Verify gh-pages branch exists
- Ensure workflow has write permissions
- Clear browser cache

### Import Errors

**Problem**: Module not found errors

**Solution**:
```powershell
pip install -r requirements.txt --upgrade
```

## Dependencies

- **requests** (2.31.0+): GitHub API communication
- **plotly** (5.18.0+): Interactive visualizations
- **pandas** (2.1.0+): Data processing
- **pyyaml** (6.0.1+): Configuration parsing
- **jinja2** (3.1.2+): HTML templating
- **python-dateutil** (2.8.2+): Date handling

## Development

### Adding New Metrics

1. **Fetch data** in `fetch_github_data.py`:
   ```python
   def get_new_metric(self, repo_name: str) -> Dict:
       url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/endpoint"
       return self._make_request(url)
   ```

2. **Create visualization** in `generate_dashboard.py`:
   ```python
   def create_new_metric_chart(self, data: Dict) -> str:
       # Chart logic
       return fig.to_html(full_html=False, include_plotlyjs='cdn')
   ```

3. **Add to dashboard** in HTML template

### Testing Locally

```powershell
# Test data fetching
python fetch_github_data.py

# Test dashboard generation
python generate_dashboard.py

# Open in browser
start index.html
```

## Performance

- **API Calls**: Approximately 10-20 per repository
- **Rate Limits**: 5000/hour with token, 60/hour without
- **Generation Time**: 1-3 minutes for 4 repositories
- **Dashboard Size**: Approximately 2-5 MB HTML file

## Security

- **GitHub Token**: Never commit tokens to repository
- **Use secrets**: Store in GitHub Secrets for Actions
- **Environment variables**: Use `.env` file for local development (git-ignored)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review GitHub Actions logs for errors

## Roadmap

Future enhancements:
- [ ] Historical trend tracking
- [ ] Comparison with other organizations
- [ ] Email notifications on significant changes
- [ ] Custom metric definitions
- [ ] Export to PDF/PNG
- [ ] Mobile app view
- [ ] Real-time updates via webhooks

## Acknowledgments

- Built with Plotly for interactive visualizations
- Deployed via GitHub Pages
- Automated with GitHub Actions
- Inspired by modern tech dashboard designs
