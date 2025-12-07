# research-page-generator

Toolkit for generating professional GitHub Pages sites for research projects

[View on GitHub](https://github.com/Digital-AI-Finance/research-page-generator){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | SCSS |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-12-04 |
| Last Updated | 2025-12-06 |
| Last Push | 2025-12-06 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | private |






## Datasets

This repository includes 8 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [funding.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/sample/_data/funding.json) | .json | 1.22 KB |

| [news.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/sample/_data/news.json) | .json | 1.65 KB |

| [publications.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/sample/_data/publications.json) | .json | 5.13 KB |

| [team.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/sample/_data/team.json) | .json | 2.1 KB |

| [funding.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/template/_data/funding.json) | .json | 0.52 KB |

| [news.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/template/_data/news.json) | .json | 0.5 KB |

| [publications.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/template/_data/publications.json) | .json | 0.61 KB |

| [team.json](https://github.com/Digital-AI-Finance/research-page-generator/blob/main/template/_data/team.json) | .json | 0.98 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# Research Project Page Generator

A complete toolkit for generating professional GitHub Pages sites for research projects. Based on the [Network-Based Credit Risk Models](https://digital-ai-finance.github.io/network-based-credit-risk-models/) project.

## Features

- **Professional Design**: Navy/gold color scheme with responsive layout
- **Dark Mode**: User-toggleable dark/light theme with localStorage persistence
- **Mobile-First**: Hamburger menu and responsive grid layouts
- **Publications**: Auto-fetched from OpenAlex.org with BibTeX export
- **Search**: Full-text search using Lunr.js
- **Analytics**: Publications chart (Chart.js) and co-authorship network (D3.js)
- **SEO Ready**: Schema.org structured data, meta tags, sitemap, RSS feed
- **Sections**: Home, Team, Research, Publications, Analytics, Resources, News, Events, Collaborations, Funding, Contact

## Quick Start

### Option 1: Use with Claude

1. Copy `PROMPT.md` content
2. Start a new conversation with Claude
3. Paste the prompt and provide your project details
4. Claude will generate a complete site customized for your project

### Option 2: Manual Setup

1. Copy the `template/` folder to your new repository
2. Replace all `{{PLACEHOLDER}}` values in the files
3. Update `_data/*.json` files with your content
4. Push to GitHub and enable Pages

## File Structure

```
research-page-generator/
+-- PROMPT.md                    # Claude prompt for site generation
+-- README.md                    # This file
+-- template/
    +-- _config.yml              # Jekyll configuration
    +-- index.md                 # Main page with all sections
    +-- feed.xml                 # RSS feed (create if needed)
    +-- _data/
    |   +-- team.json            # Team member profiles
    |   +-- publications.json    # Publication list
    |   +-- news.json            # News/updates
    |   +-- funding.json         # Funding sources
    +-- assets/
    |   +-- css/
    |   |   +-- style.scss       # All styles with dark mode
    |   +-- js/
    |   |   +-- main.js          # Core functionality
    |   |   +-- visualizations.js# Charts and graphs
    |   +-- images/
    |       +-- logos/           # Institution logos
    +-- scripts/
        +-- fetch_publications.py # OpenAlex publication fetcher
        +-- verify_site.py       # Site verification tool
```

## Configuration Guide

### 1. Jekyll Config (`_config.yml`)

Update these key settings:

```yaml
title: "Your Project Title"
description: "Your project description"
baseurl: "/your-repo-name"
url: "https://your-org.github.io"
author: "Principal Investigator Name"
```

### 2. Team Data (`_data/team.json`)

```json
[
  {
    "name": "Prof. Dr. Name",
    "role": "Principal Investigator",
    "institution": "University Name",
    "bio": "Research focus description",
    "image": "images/photo.jpg",
    "orcid": "0000-0000-0000-0000",
    "google_scholar": "https://scholar.google.com/...",
    "linkedin": "https://linkedin.com/in/...",
    "website": "https://..."
  }
]
```

### 3. Publications (`_data/publications.json`)

Auto-fetch using the Python script:

```bash
# 1. Edit scripts/fetch_publications.py
# 2. Update TEAM_MEMBERS and CONTACT_EMAIL
# 3. Run:
python scripts/fetch_publications.py
```

Or manually add entries:

```json
[
  {
    "title": "Publication Title",
    "authors": "Author1, A., Author2, B.",
    "journal": "Journal Name",
    "year": 2024,
    "doi": "10.xxxx/xxxxx",
    "citations": 10,
    "open_access": true,
    "abstract": "Optional abstract text"
  }
]
```

### 4. News (`_data/news.json`)

```json
[
  {
    "date": "2024-12-01",
    "title": "News Title",
    "description": "News description text."
  }
]
```

### 5. Funding (`_data/funding.json`)

```json
[
  {
    "title": "Grant Title",
    "funder": "Funding Agency",
    "amount": "100,000 CHF",
    "grant_number": "12345",
    "period": "2024-01 - 2027-12",
    "institution": "Host Institution",
    "team": "PI Name (PI); Researcher Names"
  }
]
```

## Customization

### Colors

Edit CSS variables in `assets/css/style.scss`:

```scss
:root {
  --primary-color: #1a365d;      // Main brand color
  --primary-dark: #0f2942;        // Darker shade
  --accent-color: #c9a227;        // Highlight color
  --accent-light: #f4e4bc;        // Light accent
}
```

### Publication Filters

Edit topic keywords in `assets/js/main.js`:

```javascript
const topicKeywords = {
  'topic1': ['keyword1', 'keyword2'],
  'topic2': ['keyword3', 'keyword4'],
  // Add your research topics
};
```

### Network Graph

Edit nodes and links in `assets/js/visualizations.js`:

```javascript
const nodes = [
  { id: 'PI', name: 'Principal Investigator', group: 1 },
  { id: 'R1', name: 'Researcher 1', group: 1 },
  // Add team members
];

const links = [
  { source: 'PI', target: 'R1', value: 5 },
  // Add collaboration connections
];
```

### Contact Form

The template uses [Formspree](https://formspree.io/) for contact forms:

1. Create a free Formspree account
2. Get your form endpoint
3. Update the form action in `index.md`:

```html
<form action="https://formspree.io/f/YOUR_ID" method="POST">
```

## Deployment

### GitHub Pages

1. Push your repository to GitHub
2. Go to Settings > Pages
3. Select "Deploy from a branch"
4. Choose `main` branch, `/ (root)` folder
5. Save and wait for deployment

### Local Development

```bash
# Install Jekyll
gem install bundler jekyll

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Open http://localhost:4000/your-repo-name/
```

## Python Scripts

### fetch_publications.py

Fetches publications from OpenAlex.org:

```bash
# Install dependencies
pip install requests

# Configure team members in the script
# Run
python scripts/fetch_publications.py
```

### verify_site.py

Comprehensive site verification:

```bash
# Install dependencies
pip install requests playwright
playwright install chromium

# Configure SITE_URL in the script
# Run
python scripts/verify_site.py
```

## Placeholders Reference

Key placeholders to replace in `index.md`:

| Placeholder | Description |
|-------------|-------------|
| `{{PROJECT_TITLE}}` | Full project title |
| `{{PROJECT_DESCRIPTION}}` | SEO description |
| `{{GITHUB_ORG}}` | GitHub organization name |
| `{{REPO_NAME}}` | Repository name |
| `{{PI_NAME}}` | Principal investigator name |
| `{{PI_INSTITUTION}}` | PI's institution |
| `{{PROJECT_FUNDER}}` | Main funding agency |
| `{{GRANT_NUMBER}}` | Grant/project number |
| `{{GRANT_AMOUNT}}` | Total funding amount |
| `{{START_DATE}}` | Project start date |
| `{{END_DATE}}` | Project end date |

## License

MIT License - Feel free to use for any research project.

## Credits

Based on the SNSF-funded "Network-Based Credit Risk Models in P2P Lending Markets" project by Prof. Dr. Joerg Osterrieder at Bern University of Applied Sciences.
