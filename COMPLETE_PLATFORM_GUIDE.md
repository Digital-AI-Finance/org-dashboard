# Complete Research Platform Guide

## Live Demo

**Live Platform**: https://digital-ai-finance.github.io/org-dashboard/

See the platform in action with 4 example repositories demonstrating all research features:
- Publication tracking with DOI/arXiv integration
- Reproducibility scoring and badges
- Community verification with replication attempts
- Interactive visualizations

## Overview

This comprehensive research platform extends your GitHub organization dashboard into a full-featured **Quantlet-style research catalog** with all 6 phases implemented:

1. Enhanced Data Extraction
2. Notebook Rendering
3. Citation Tracking
4. Advanced Search
5. Interactive Visualizations
6. Community Features

## Architecture

```
Digital-AI-Finance Research Platform
│
├── Data Layer
│   ├── fetch_org_data_research.py - Enhanced GitHub API fetcher
│   ├── parse_research_metadata.py - README/metadata parser
│   └── fetch_academic_data.py - arXiv/CrossRef integration
│
├── Analysis Layer
│   ├── citation_tracker.py - Citation graphs & impact metrics
│   ├── search_indexer.py - Full-text search index
│   └── community_features.py - Replication & verification
│
├── Visualization Layer
│   ├── render_notebooks.py - Jupyter → HTML conversion
│   └── visualization_builder.py - Plotly charts & networks
│
├── Orchestration
│   └── build_research_platform.py - Master build script
│
└── Output
    ├── data/ - JSON data files
    ├── docs/ - Generated markdown & HTML
    └── docs/visualizations/ - Interactive charts
```

## Quick Start

### One-Command Build

```bash
# Set your credentials
export GITHUB_TOKEN='your_personal_access_token'
export GITHUB_ORG='Digital-AI-Finance'

# Build everything
python scripts/build_research_platform.py Digital-AI-Finance
```

This will:
1. Fetch all repos with research metadata
2. Build citation network
3. Create search index
4. Generate visualizations
5. Calculate reproducibility scores

### Incremental Build

Skip phases you don't need:

```bash
# Skip visualizations and community features
python scripts/build_research_platform.py Digital-AI-Finance \
  --skip visualizations community
```

## Phase Details

### Phase 1: Enhanced Data Extraction

**What it does:**
- Fetches repo metadata from GitHub API
- Extracts DOIs, arXiv IDs, SSRN IDs from READMEs
- Identifies authors, citations, datasets
- Detects Jupyter notebooks and R Markdown files
- Checks for Docker, requirements.txt, environment.yml

**Run individually:**
```bash
python scripts/fetch_org_data_research.py
```

**Output:**
- `data/repos.json` - Full repository data
- `data/stats.json` - Organization statistics
- `data/research_metadata.json` - Research-specific data

**Key features:**
- DOI pattern matching: `10.\d{4,9}/[-._;()/:a-zA-Z0-9]+`
- arXiv extraction: `arXiv:\s*(\d{4}\.\d{4,5})`
- Author parsing from README sections
- Dataset detection by file extension and folder name
- Notebook discovery (.ipynb, .Rmd)

---

### Phase 2: Notebook Rendering

**What it does:**
- Converts Jupyter notebooks to standalone HTML
- Extracts figures/images from notebook outputs
- Extracts tables (pandas DataFrames)
- Creates notebook index pages

**Run individually:**
```bash
python scripts/render_notebooks.py
```

**Output:**
- `docs/notebooks/{repo}_{notebook}.html` - Rendered notebooks
- `docs/notebooks/figures/` - Extracted figures
- `docs/notebooks/{repo}_index.md` - Notebook catalog

**Features:**
- Uses nbconvert with classic template
- Syntax highlighting preserved
- Outputs (plots, tables) embedded
- Optional notebook execution (disabled by default for safety)

---

### Phase 3: Citation Tracking

**What it does:**
- Builds citation graph between repositories
- Tracks internal citations (repo→repo)
- Fetches external citations from CrossRef
- Calculates h-index per repo
- Monitors citation growth over time

**Run individually:**
```bash
python scripts/citation_tracker.py
```

**Output:**
- `data/citation_report.json` - Full citation analysis
- `data/citation_history.json` - Historical tracking

**Metrics calculated:**
- Internal citations (from other org repos)
- External citations (from academic databases)
- H-index per repository
- Citation growth trends
- Network centrality

**Network statistics:**
- Most cited repositories
- Most citing repositories
- Average citations per repo
- Citation network density

---

### Phase 4: Advanced Search

**What it does:**
- Full-text indexing of READMEs, papers, research metadata
- Inverted index for fast searching
- Faceted navigation (filter by language, topic, year, etc.)
- Autocomplete suggestions

**Run individually:**
```bash
python scripts/search_indexer.py
```

**Output:**
- `data/search_index.pkl` - Serialized search index

**Search features:**
- Boolean AND queries (all terms must match)
- TF-IDF relevance scoring
- Title/metadata boosting
- Facet filtering
- Stop word removal
- Autocomplete on indexed terms

**Example usage:**
```python
from search_indexer import SearchIndex

index = SearchIndex.load_index()
results = index.search(
    query="machine learning trading",
    filters={'language': 'python', 'year': '2024'},
    limit=10
)
```

**Facets available:**
- type (readme, publication, research)
- repo (repository name)
- language (programming language)
- topics (GitHub topics)
- year (publication year)
- authors
- keywords

---

### Phase 5: Interactive Visualizations

**What it does:**
- Creates interactive Plotly charts
- Builds citation network graphs
- Generates publication timelines
- Shows language distribution
- Creates collaboration networks

**Run individually:**
```bash
python scripts/visualization_builder.py
```

**Output:**
- `docs/visualizations/citation_network.html` - Interactive network
- `docs/visualizations/publication_timeline.html` - Timeline chart
- `docs/visualizations/research_impact.html` - Impact metrics
- `docs/visualizations/language_distribution.html` - Pie chart
- `docs/visualizations/collaboration_network.json` - Network data

**Visualizations:**

1. **Citation Network**
   - Nodes: Repositories
   - Edges: Citations between repos
   - Node size: Number of citations
   - Interactive hover: Repo name, citations

2. **Publication Timeline**
   - X-axis: Years
   - Y-axis: Number of publications
   - Bar chart of research output over time

3. **Research Impact**
   - 3 subplots: Internal citations, External citations, H-index
   - Bar charts per repository
   - Compare impact across repos

4. **Language Distribution**
   - Pie chart of programming languages
   - Shows diversity of technical stack

5. **Collaboration Network**
   - Nodes: Repositories
   - Edges: Shared authors
   - Edge weight: Number of shared authors
   - Identifies research collaborations

---

### Phase 6: Community Features

**What it does:**
- Tracks replication attempts (success/partial/fail)
- Community verification system (peer reviews)
- Calculates reproducibility scores
- Generates reproducibility badges

**Run individually:**
```bash
python scripts/community_features.py
```

**Output:**
- `data/replications.json` - Replication tracking
- `data/verifications.json` - Community reviews
- `data/reproducibility_report.json` - Scores & badges

**Reproducibility Scoring:**

Total: 100 points

- **Documentation (30 pts)**
  - README present: 10 pts
  - Abstract: 10 pts
  - Publications: 10 pts

- **Environment (25 pts)**
  - requirements.txt: 10 pts
  - Dockerfile: 10 pts
  - environment.yml: 5 pts

- **Data (20 pts)**
  - Datasets present: 10 pts
  - Multiple datasets: 10 pts

- **Code (15 pts)**
  - Notebooks: 10 pts
  - Wiki: 5 pts

- **Community (10 pts)**
  - Based on verification ratings

**Badge levels:**
- Gold: 80+ points
- Silver: 60-79 points
- Bronze: 40-59 points
- None: <40 points

**Replication tracking:**
```python
from community_features import ReplicationTracker

tracker = ReplicationTracker()
tracker.add_replication_attempt(
    repo_name='ai-trading-bot',
    user='researcher_x',
    status='success',  # or 'partial', 'failed'
    notes='Replicated on Ubuntu 22.04',
    environment={'os': 'Ubuntu 22.04', 'python': '3.11'}
)
```

**Verification system:**
```python
from community_features import VerificationSystem

verifier = VerificationSystem()
verifier.add_verification(
    repo_name='ai-trading-bot',
    reviewer='expert_reviewer',
    category='code_quality',  # or 'documentation', 'reproducibility'
    rating=4,  # 1-5
    comments='Well-structured code, good documentation'
)
```

---

## Data Flow

```
GitHub API → fetch_org_data_research.py
    ↓
repos.json
    ↓
    ├─→ citation_tracker.py → citation_report.json
    ├─→ search_indexer.py → search_index.pkl
    ├─→ visualization_builder.py → visualizations/*.html
    └─→ community_features.py → reproducibility_report.json
```

## Generated Files

### Data Files (`data/`)
- `repos.json` - All repository data with research metadata
- `stats.json` - Organization-wide statistics
- `research_metadata.json` - Research-specific metadata only
- `citation_report.json` - Citation analysis
- `citation_history.json` - Historical citation data
- `search_index.pkl` - Serialized search index
- `reproducibility_report.json` - Scores and badges
- `replications.json` - Replication attempts
- `verifications.json` - Community reviews
- `build_log.json` - Build process log

### Documentation (`docs/`)
- `index.md` - Homepage
- `stats.md` - Statistics page
- `repos/*.md` - Individual repository pages
- `by-language/*.md` - Language categories
- `by-topic/*.md` - Topic categories

### Visualizations (`docs/visualizations/`)
- `citation_network.html` - Interactive network
- `publication_timeline.html` - Timeline chart
- `research_impact.html` - Impact metrics
- `language_distribution.html` - Language pie chart
- `collaboration_network.json` - Network data
- `figures/` - Extracted notebook figures

### Notebooks (`docs/notebooks/`)
- `{repo}_{notebook}.html` - Rendered notebooks
- `{repo}_index.md` - Notebook catalog
- `figures/` - Extracted figures

## Configuration

### Environment Variables

```bash
# Required
GITHUB_TOKEN='ghp_xxx'  # Personal access token
GITHUB_ORG='Digital-AI-Finance'  # Organization name

# Optional
ENRICH_ACADEMIC='true'  # Fetch from arXiv/CrossRef (default: true)
```

### GitHub Actions Integration

Update `.github/workflows/update-dashboard.yml`:

```yaml
- name: Build research platform
  env:
    GITHUB_TOKEN: ${{ secrets.GH_PAT }}
    GITHUB_ORG: ${{ secrets.ORG_NAME }}
    ENRICH_ACADEMIC: 'true'
  run: |
    python scripts/build_research_platform.py ${{ secrets.ORG_NAME }}
```

## Performance

### Timing (approximate)

For organization with 10 repositories:

- Phase 1 (Data fetch): 2-5 minutes
- Phase 2 (Notebooks): 30 seconds
- Phase 3 (Citations): 10 seconds
- Phase 4 (Search): 5 seconds
- Phase 5 (Visualizations): 15 seconds
- Phase 6 (Community): 5 seconds

**Total: ~3-6 minutes**

### Rate Limits

- GitHub API: 5000 requests/hour (authenticated)
- arXiv API: No strict limit, 1 req/sec recommended
- CrossRef API: No limit for polite usage

## Troubleshooting

### Common Issues

**1. Import errors**
```bash
# Install all dependencies
pip install -r requirements.txt
```

**2. No repos found**
- Check GITHUB_ORG is correct
- Verify token has org access
- Check token scopes (need `repo`, `read:org`)

**3. Plotly visualizations not generating**
```bash
pip install plotly kaleido
```

**4. Search index not loading**
- Run search_indexer.py first
- Check data/search_index.pkl exists

**5. Citation network empty**
- Repos need publications with DOIs/arXiv
- Repos must cite each other
- Check data/citation_report.json

## Advanced Usage

### Custom Filtering

```python
# Only process repos with papers
repos_with_papers = [
    repo for repo in repos_data
    if repo.get('research_metadata', {}).get('publications')
]
```

### Selective Phase Execution

```bash
# Only build citations and visualizations
python scripts/build_research_platform.py Digital-AI-Finance \
  --skip fetch_data search community
```

### Integration with Existing Dashboard

```python
# In generate_markdown.py, use research template
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('repo_research.md.j2')  # Use research template

for repo in repos:
    content = template.render(repo=repo)
    # Write to docs/
```

## API Reference

### Citation Tracker

```python
from citation_tracker import CitationGraph

graph = CitationGraph()
graph_data = graph.build_graph(repos_data)
impact = graph.calculate_impact_metrics()
stats = graph.get_citation_network_stats()
```

### Search Index

```python
from search_indexer import SearchIndex

index = SearchIndex()
doc_id = index.add_document(content, metadata)
results = index.search(query, filters, limit)
facets = index.get_facets(query)
suggestions = index.autocomplete(prefix, limit)
```

### Visualization Builder

```python
from visualization_builder import VisualizationBuilder

builder = VisualizationBuilder(output_dir='docs/visualizations')
builder.create_citation_network(citation_graph)
builder.create_publication_timeline(repos_data)
builder.create_research_impact_chart(impact_metrics)
```

### Community Features

```python
from community_features import (
    ReplicationTracker,
    VerificationSystem,
    ReproducibilityScorer
)

tracker = ReplicationTracker()
verifier = VerificationSystem()
scorer = ReproducibilityScorer()

score_data = scorer.calculate_score(repo_data)
```

## Maintenance

### Regular Updates

Run weekly or monthly:
```bash
python scripts/build_research_platform.py Digital-AI-Finance
```

### Citation History

Accumulates over time in `data/citation_history.json`:
- Track citation growth
- Monitor research impact trends
- Identify emerging repos

### Search Index Rebuilding

Rebuild after major changes:
```bash
python scripts/search_indexer.py
```

## Future Enhancements

Potential additions:
- Google Scholar integration for citation tracking
- Semantic Scholar API for paper recommendations
- GitHub Discussions integration for Q&A
- Code Ocean integration for computational reproducibility
- Zenodo integration for dataset DOIs
- ORCID integration for author disambiguation

## Support

For issues:
1. Check this documentation
2. Review script docstrings
3. Examine example output in `data/`
4. Check build log: `data/build_log.json`

## License

MIT License - Same as main dashboard
