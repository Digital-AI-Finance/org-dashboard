# hugo-research-template

Hugo template for research project websites with GitHub Pages

[View on GitHub](https://github.com/Digital-AI-Finance/hugo-research-template){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | CSS |
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
| Visibility | public |






## Datasets

This repository includes 11 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [data](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data) |  | 0.0 KB |

| [about.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/about.yaml) | .yaml | 0.87 KB |

| [collaborations.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/collaborations.yaml) | .yaml | 0.46 KB |

| [events.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/events.yaml) | .yaml | 0.5 KB |

| [funders.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/funders.yaml) | .yaml | 0.51 KB |

| [news.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/news.yaml) | .yaml | 0.63 KB |

| [partners.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/partners.yaml) | .yaml | 0.46 KB |

| [publications.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/publications.yaml) | .yaml | 1.95 KB |

| [stats.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/stats.yaml) | .yaml | 0.21 KB |

| [team.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/team.yaml) | .yaml | 1.12 KB |

| [timeline.yaml](https://github.com/Digital-AI-Finance/hugo-research-template/blob/main/data/timeline.yaml) | .yaml | 0.78 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Enabled

## README

# Hugo Research Project Website Template

A clean, professional Hugo template for research project websites with a fixed left sidebar navigation.

## Features

- Fixed left sidebar navigation (140px)
- Responsive design (sidebar hides below 900px)
- Multiple section types pre-styled
- Easy color customization via CSS variables
- GitHub Pages compatible (with GitHub Actions)

## Quick Start

1. Copy this entire folder to your new project
2. Update `hugo.toml` with your project details
3. Modify `layouts/index.html` with your content
4. Run `hugo server` for local development
5. Push to GitHub and configure GitHub Actions

## Local Development

```bash
# Install Hugo (https://gohugo.io/installation/)
# Windows: winget install Hugo.Hugo.Extended
# Mac: brew install hugo

# Serve locally with live reload
hugo server -D

# Build for production
hugo --minify
```

The site is served at `http://localhost:1313/` by default.

## File Structure

```
hugo-research-template/
├── hugo.toml              # Hugo configuration
├── layouts/
│   ├── _default/
│   │   └── baseof.html    # Base layout with sidebar
│   └── index.html         # Homepage content
├── static/
│   └── css/
│       └── style.css      # All styles
├── content/
│   └── _index.md          # Homepage metadata
└── README.md              # This file
```

## Configuration (hugo.toml)

Update these values:

```toml
baseURL = "https://yourusername.github.io/your-repo-name/"
title = "Your Project Title"

[params]
  description = "Brief description for SEO"
  badge1 = "Research Project"
  badge2 = "2024-2027"
  author = "Dr. Your Name"
  email = "email@university.edu"
  institution = "Department Name"
  university = "University Name"
  location = "City, Country"
```

## GitHub Pages Deployment

Create `.github/workflows/hugo.yml`:

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.128.0
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb
      - name: Checkout
        uses: actions/checkout@v4
      - name: Build with Hugo
        run: hugo --minify
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## Customization

### Colors (static/css/style.css)

Edit the CSS variables at the top of `style.css`:

```css
:root {
    --primary-color: #2d3748;      /* Dark gray - headers, sidebar */
    --primary-light: #4a5568;      /* Lighter gray - hover states */
    --accent-color: #805ad5;       /* Purple - accents, badges */
    --text-color: #2d3748;         /* Dark gray - body text */
}
```

### Navigation Links (layouts/_default/baseof.html)

Add or remove navigation links in the sidebar section.

## Dependencies

The template uses these external resources (loaded via CDN):

- Google Fonts: Inter
- Font Awesome 6.4.0 (icons)

## License

Free to use for any research project.
