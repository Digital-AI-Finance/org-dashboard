# Research Platform Features

This document describes the **Quantlet-style research features** added to the Digital-AI-Finance GitHub Organization Dashboard.

## Overview

The dashboard has been extended from a simple repository catalog into a comprehensive **research platform** for reproducible quantitative finance research, inspired by Quantlet.com.

## What's Been Built

### Phase 1: Enhanced Data Extraction (COMPLETED)

#### 1. Research Metadata Schema
**File**: `schemas/research_metadata_schema.json`

Comprehensive JSON schema defining structure for:
- Research project metadata (title, abstract, authors, keywords)
- Publications (DOI, arXiv, SSRN links)
- Datasets (location, format, size)
- Code artifacts (notebooks, dependencies)
- Reproducibility indicators
- Citation information

#### 2. Research Metadata Parser
**File**: `scripts/parse_research_metadata.py`

Extracts research information from repositories:
- **DOI extraction**: Finds DOIs in README using regex patterns
- **arXiv ID extraction**: Identifies arXiv preprints
- **SSRN extraction**: Detects working papers
- **Author parsing**: Extracts author names, emails, affiliations
- **BibTeX citations**: Finds and extracts bibliography entries
- **Keywords/topics**: Identifies research keywords
- **Abstract extraction**: Pulls research abstracts from READMEs
- **Dataset detection**: Finds CSV, Excel, JSON, Parquet files
- **Notebook detection**: Identifies Jupyter and R Markdown notebooks
- **Reproducibility check**: Detects requirements.txt, Dockerfile, environment.yml

#### 3. Academic API Integration
**File**: `scripts/fetch_academic_data.py`

Fetches metadata from external sources:
- **arXiv API**: Paper titles, abstracts, authors, categories, publication dates
- **CrossRef API**: DOI metadata, citation counts, journal info, references
- **SSRN**: Basic working paper info (limited, no official API)

Features:
- Rate limiting to respect API limits
- Caching to avoid redundant requests
- Error handling for missing/invalid identifiers
- Enrichment of publication data with external metadata

#### 4. Enhanced Data Fetcher
**File**: `scripts/fetch_org_data_research.py`

Extended version of original fetcher with:
- Calls research metadata parser for each repository
- Fetches repository contents for deeper analysis
- Integrates academic API data
- Saves three data files:
  - `data/repos.json` - Full repository data with research metadata
  - `data/stats.json` - Statistics including research metrics
  - `data/research_metadata.json` - Separate research-only data

New statistics tracked:
- Repos with publications
- Repos with notebooks
- Repos with datasets
- Total publications count
- Total notebooks count

#### 5. Enhanced Repository Template
**File**: `templates/repo_research.md.j2`

New template displaying:
- **Publications section**: DOI, arXiv, SSRN links with metadata
- **Authors**: Name, affiliation from papers
- **Citation counts**: From CrossRef
- **Notebooks**: List of Jupyter/R Markdown files
- **Datasets**: Table of data files with sizes
- **Reproducibility**: Badge showing available tools
- **Research keywords**: Extracted topics
- Original repository info (stars, forks, etc.)

## How to Use

### Basic Usage

```bash
# Set environment variables
export GITHUB_TOKEN='your_token'
export GITHUB_ORG='Digital-AI-Finance'

# Run enhanced fetcher with research metadata
python scripts/fetch_org_data_research.py
```

### With Academic Enrichment

```bash
# Enable external API calls (arXiv, CrossRef)
export ENRICH_ACADEMIC='true'
python scripts/fetch_org_data_research.py
```

### Disable Academic Enrichment

```bash
# Skip external API calls (faster, but less metadata)
export ENRICH_ACADEMIC='false'
python scripts/fetch_org_data_research.py
```

## Data Structure

### Research Metadata Format

```json
{
  "repo_name": "ai-trading-bot",
  "research": {
    "title": "Deep Learning for Algorithmic Trading",
    "abstract": "We propose a novel LSTM architecture...",
    "authors": [
      {
        "name": "John Doe",
        "email": "john@example.com",
        "affiliation": "MIT"
      }
    ],
    "keywords": ["deep-learning", "trading", "lstm"]
  },
  "publications": [
    {
      "type": "preprint",
      "arxiv_id": "2024.12345",
      "title": "Predicting Stock Prices with LSTMs",
      "abstract": "...",
      "authors": [...],
      "year": 2024,
      "citation_count": 15
    }
  ],
  "datasets": [
    {
      "name": "sp500_prices.csv",
      "path": "data/sp500_prices.csv",
      "format": ".csv",
      "size_bytes": 1048576
    }
  ],
  "code": {
    "notebooks": [
      {
        "path": "analysis.ipynb",
        "title": "analysis",
        "language": "python",
        "type": "jupyter"
      }
    ]
  },
  "reproducibility": {
    "has_requirements": true,
    "has_dockerfile": true,
    "replication_status": "not_attempted"
  }
}
```

## Key Features

### 1. Publication Discovery
- Automatically finds DOIs, arXiv IDs, SSRN IDs in READMEs
- Fetches full paper metadata from academic databases
- Displays citation counts
- Links to paper PDFs

### 2. Code & Data Catalog
- Lists all notebooks (Jupyter, R Markdown)
- Catalogs datasets with format and size
- Identifies main analysis scripts
- Tracks dependencies (requirements.txt)

### 3. Reproducibility Assessment
- Checks for Docker, environment files, Makefiles
- Can link to Binder/Colab for one-click reproduction
- Shows which tools are available

### 4. Research Analytics
- Organization-level stats on publications
- Track how many repos have papers
- Monitor notebook/dataset availability
- Can be extended to track citations over time

## What's Next (Future Phases)

### Phase 2: Notebook Rendering (TODO)
- Convert Jupyter notebooks to HTML using nbconvert
- Display notebook outputs directly in dashboard
- Extract figures and tables automatically
- Show code with syntax highlighting

### Phase 3: Citation Tracking (TODO)
- Build citation graph between repositories
- Track external citations via Google Scholar
- Display citation networks
- Monitor research impact over time

### Phase 4: Advanced Search (TODO)
- Full-text search across READMEs and notebooks
- Filter by methodology, dataset, citation count
- Faceted navigation
- Research timeline view

### Phase 5: Interactive Visualizations (TODO)
- Embed Plotly/Bokeh charts from notebooks
- Research collaboration networks
- Citation impact visualizations
- Aggregate results dashboards

### Phase 6: Community Features (TODO)
- Replication attempts tracking
- Community verification system
- Reproducibility scores
- Discussion and comments

## Configuration

### Environment Variables

```bash
# Required
GITHUB_TOKEN          # GitHub personal access token
GITHUB_ORG           # Organization name

# Optional
ENRICH_ACADEMIC      # Enable academic API calls (default: true)
```

### GitHub Actions Integration

Update `.github/workflows/update-dashboard.yml` to use the research-enhanced fetcher:

```yaml
- name: Fetch organization data
  env:
    GITHUB_TOKEN: ${{ secrets.GH_PAT }}
    GITHUB_ORG: ${{ secrets.ORG_NAME }}
    ENRICH_ACADEMIC: 'true'
  run: |
    python scripts/fetch_org_data_research.py
```

## API Rate Limits

### GitHub API
- 5000 requests/hour for authenticated requests
- Research fetcher uses ~10-20 requests per repo
- Should handle 250-500 repos easily

### arXiv API
- No official rate limit
- Recommended: 1 request/second
- Current implementation: 0.5 second delay

### CrossRef API
- Polite pool: No strict limits if you include email
- Current implementation: 0.5 second delay
- Free and unrestricted for scholarly use

## Dependencies

Added to `requirements.txt`:
- `nbconvert>=7.16.0` - Jupyter notebook rendering (for Phase 2)
- `nbformat>=5.9.0` - Notebook format handling
- `requests>=2.31.0` - HTTP requests for APIs

## Files Created

### Core System
- `schemas/research_metadata_schema.json` - Metadata schema
- `scripts/parse_research_metadata.py` - Metadata extraction
- `scripts/fetch_academic_data.py` - External API integration
- `scripts/fetch_org_data_research.py` - Enhanced data fetcher
- `templates/repo_research.md.j2` - Research-enhanced template

### Documentation
- `RESEARCH_FEATURES.md` - This file

## Testing

Test the metadata parser:
```bash
python scripts/parse_research_metadata.py
```

Test academic API fetcher:
```bash
python scripts/fetch_academic_data.py
```

Test full system on your organization:
```bash
export GITHUB_TOKEN='your_token'
export GITHUB_ORG='Digital-AI-Finance'
python scripts/fetch_org_data_research.py
```

## Example Output

When you run the enhanced fetcher, you'll see:

```
====================================================================
GitHub Organization Data Fetcher (with Research Metadata)
====================================================================

Fetching data for organization: Digital-AI-Finance
Academic enrichment: enabled
Authenticated as: josterri
Organization found: Digital-AI-Finance

Fetching repositories...
Found 1 repositories

Fetching detailed data for each repository...
Processing repos: 100%
  Extracting research metadata...

Successfully fetched data for 1 repositories

Enriching with academic database information...
Academic enrichment: 100%
Fetching arXiv: 2024.12345
Fetching DOI: 10.1234/example.2024

Calculating statistics...

Summary:
  - Total repositories: 1
  - Active repositories: 1
  - Total stars: 342
  - Total forks: 87
  - Repos with publications: 1
  - Repos with notebooks: 2
  - Total publications: 2

Data saved to:
  - data/repos.json
  - data/stats.json
  - data/research_metadata.json
```

## Notes

- **Privacy**: All data is extracted from public GitHub repositories
- **Cache**: Consider implementing caching for academic API calls
- **Performance**: Research extraction adds ~2-5 seconds per repo
- **Updates**: Academic data should be refreshed periodically (e.g., monthly)
- **Accuracy**: Metadata extraction uses heuristics and may not be 100% accurate

## Roadmap

- [x] Phase 1: Enhanced Data Extraction
- [ ] Phase 2: Notebook Rendering
- [ ] Phase 3: Citation Tracking
- [ ] Phase 4: Advanced Search
- [ ] Phase 5: Interactive Visualizations
- [ ] Phase 6: Community Features

## Support

For issues or questions about research features:
- Check this documentation
- Review code comments in scripts
- Examine example output in `data/` directory
- Test with individual scripts before full integration

## License

Same as main dashboard (MIT License)
