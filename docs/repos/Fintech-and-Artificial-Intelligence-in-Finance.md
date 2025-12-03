# Fintech-and-Artificial-Intelligence-in-Finance

Archive of COST Action CA19130 - FinAI: Fintech and Artificial Intelligence in Finance (2020-2024)

[View on GitHub](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | HTML |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-12-02 |
| Last Updated | 2025-12-02 |
| Last Push | 2025-12-02 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | private |






## Datasets

This repository includes 11 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [deep_crawl_report.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/deep_crawl_report.json) | .json | 5.49 KB |

| [deep_crawl_v2_report.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/deep_crawl_v2_report.json) | .json | 4.68 KB |

| [deep_crawl_verification.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/deep_crawl_verification.json) | .json | 32.31 KB |

| [download_progress.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/download_progress.json) | .json | 0.65 KB |

| [gdrive_auth_download_report.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/gdrive_auth_download_report.json) | .json | 10.95 KB |

| [gdrive_download_report.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/gdrive_download_report.json) | .json | 24.99 KB |

| [gdrive_robust_download_report.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/gdrive_robust_download_report.json) | .json | 3.63 KB |

| [members.csv](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/members/members.csv) | .csv | 22.48 KB |

| [members.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/members/members.json) | .json | 44.37 KB |

| [urls_discovered.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/urls_discovered.json) | .json | 8.24 KB |

| [verification_report.json](https://github.com/Digital-AI-Finance/Fintech-and-Artificial-Intelligence-in-Finance/blob/main/verification_report.json) | .json | 8.16 KB |




## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# COST Action CA19130 - Fintech and Artificial Intelligence in Finance (FinAI)

Archive of materials from COST Action CA19130: "Fintech and Artificial Intelligence in Finance - Towards a transparent financial industry"

## Action Overview

| Field | Value |
|-------|-------|
| Action | CA19130 |
| Acronym | FinAI |
| Duration | 2020-09-14 to 2024-09-13 |
| Action Chair | Prof. Dr. Joerg Osterrieder |
| Countries | 51 |
| Researchers | 413 |

## Working Groups

- **WG1**: Transparency in FinTech (Machine Learning, Blockchain analytics, Big Data Mining) - Leader: Prof. Dr. Wolfgang Karl Hardle
- **WG2**: Transparent versus Black Box Decision-Support Models in the Financial Industry
- **WG3**: Transparency into Investment Product Performance for Clients - Leader: Prof. Dr. Peter Schwendner

## Repository Structure

```
Fintech-and-Artificial-Intelligence-in-Finance/
|-- downloads/
|   |-- cost_eu/              # Official COST EU page content (1 file)
|   |-- fin_ai_eu/            # Main website content (17 files)
|   |-- wiki_fin_ai_eu/       # Wiki pages as markdown (23 files)
|   |-- conference_fin_ai_eu/ # Conference materials
|   |-- ssrn_papers/          # SSRN academic papers
|   |-- academia_papers/      # Academia.edu papers
|   |-- researchgate/         # ResearchGate content
|-- publications/             # PDF publications and papers
|-- deliverables/             # COST deliverables
|-- presentations/            # Slides and presentation files
|-- videos/                   # Conference videos
|-- urls_discovered.json      # All discovered URLs
|-- scrape_cost_ca19130.py    # Web scraper script
|-- requirements.txt          # Python dependencies
```

## Primary Websites

- **COST EU Official**: https://www.cost.eu/actions/CA19130/
- **Main Website**: https://fin-ai.eu/
- **Wiki**: https://wiki.fin-ai.eu/
- **Conference**: https://conference.fin-ai.eu/
- **AI in Finance Portal**: https://www.ai-in-finance.eu/The-Digital-Finance-Research-Programme/COST-FinAI/

## Academic Publications

### SSRN Papers
1. "Exploring Research Visibility of the FinAI COST Action Members: a Bibliometric Analysis of Topics" (Abstract ID: 4616662)
2. "Mitigating Digital Asset Risks" - 30+ authors from COST Action CA19130 (Abstract ID: 4594467)

### Springer Publications
- Financial Technology: 5th International Conference, ICFT 2024
- Proceedings of International Conference on AI and Financial Innovation: AIFI 2025

## Related Projects

- MSCA Digital Finance: https://www.digital-finance-msca.com/
- BFH Project: https://www.bfh.ch/en/research/research-projects/2022-993-860-061/

## Using the Scraper

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scrape_cost_ca19130.py
```

The scraper handles:
- SSL certificate issues via curl subprocess
- Rate limiting (2 second delay between requests)
- Automatic retry on failures (3 attempts)
- HTML to Markdown conversion
- PDF and media file downloads

## License

This archive is for research and educational purposes. All original content remains the property of their respective owners.

## Acknowledgments

COST (European Cooperation in Science and Technology) is funded by the Horizon 2020 Framework Programme of the European Union.

---
*Archive created: 2025-12-02*
