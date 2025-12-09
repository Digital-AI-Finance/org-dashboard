# python-utils

Python utilities for web tools and automation

[View on GitHub](https://github.com/Digital-AI-Finance/python-utils){ .md-button .md-button--primary }


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
| Created | 2025-12-08 |
| Last Updated | 2025-12-08 |
| Last Push | 2025-12-08 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | private |








## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# Python Utils

A collection of Python utilities for web tools and automation.

## Tools

| Utility | Description |
|---------|-------------|
| [link_checker](./link_checker/) | Validate all links on a website with deep crawling |
| [quality_checker](./quality_checker/) | Check GitHub Pages quality against a reference site |
| [screenshot_checker](./screenshot_checker/) | Capture screenshots and analyze layout consistency |

## Shared Utilities

The `shared/` module provides common utilities used across tools:

- `crawler.py` - BFS page discovery, URL handling, page fetching

## Requirements

- Python 3.9+
- See individual tool READMEs for specific dependencies

## Quick Start

```bash
# Link checking
python link_checker/link_checker.py https://your-site.io

# Quality checking with subpage crawling
python quality_checker/quality_checker.py https://your-site.io --depth 2

# Screenshot and layout analysis
pip install playwright && playwright install chromium
python screenshot_checker/screenshot_checker.py https://your-site.io --depth 2
```

## License

MIT
