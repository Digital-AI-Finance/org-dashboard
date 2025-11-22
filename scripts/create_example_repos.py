#!/usr/bin/env python3
"""
Create example research repositories in the Digital-AI-Finance organization.
"""

import os
import sys

from github import Github

EXAMPLE_REPOS = [
    {
        "name": "portfolio-optimization-ml",
        "description": "Machine learning approaches to portfolio optimization using deep reinforcement learning",
        "topics": [
            "machine-learning",
            "portfolio-optimization",
            "reinforcement-learning",
            "finance",
        ],
        "readme": """# Portfolio Optimization with Deep Reinforcement Learning

This repository contains code and data for the paper "Deep Reinforcement Learning for Portfolio Optimization" (arXiv:2103.12345).

## Authors

- John Smith (University of Finance)
- Jane Doe (Tech Institute)

## Abstract

We propose a novel deep reinforcement learning approach for portfolio optimization that outperforms traditional mean-variance optimization. Our method uses a Deep Q-Network (DQN) to learn optimal trading strategies from historical market data.

## Published Paper

- **arXiv**: arXiv:2103.12345
- **DOI**: 10.1016/j.jfineco.2023.01.001
- **Published**: Journal of Financial Economics, 2023

## Citation

If you use this code or data, please cite:

```bibtex
@article{smith2023deep,
  title={Deep Reinforcement Learning for Portfolio Optimization},
  author={Smith, John and Doe, Jane},
  journal={Journal of Financial Economics},
  year={2023},
  doi={10.1016/j.jfineco.2023.01.001}
}
```

## Datasets

- `data/stock_prices.csv` - Historical stock prices (S&P 500, 2010-2023)
- `data/portfolio_returns.csv` - Simulated portfolio returns

## Requirements

```
numpy>=1.21.0
pandas>=1.3.0
tensorflow>=2.8.0
gym>=0.21.0
```

## Reproducibility

All experiments can be reproduced using:

```bash
python train_dqn.py --config configs/default.yaml
python evaluate.py --model checkpoints/best_model.h5
```

## References

This work builds on:
- Mnih et al. (2015) - Human-level control through deep reinforcement learning
- Jiang et al. (2017) - A deep reinforcement learning framework for the financial portfolio
""",
    },
    {
        "name": "credit-risk-prediction",
        "description": "Neural network models for credit risk prediction with explainable AI",
        "topics": ["credit-risk", "neural-networks", "explainable-ai", "finance"],
        "readme": """# Explainable Credit Risk Prediction

Repository for "Explainable Neural Networks for Credit Risk Assessment" (SSRN:3456789).

## Authors

- Maria Garcia (Financial Analytics Lab)
- Robert Chen (AI Research Center)

## Abstract

We develop an explainable neural network architecture for credit risk prediction that achieves state-of-the-art performance while providing interpretable feature importance scores using SHAP values.

## Published Paper

- **SSRN**: https://ssrn.com/abstract=3456789
- **DOI**: 10.2139/ssrn.3456789

## Dataset

We use the German Credit Dataset and a proprietary dataset from a major bank:
- `data/german_credit.csv` - Public German Credit Data
- `data/features.csv` - Engineered features

## Notebooks

- `notebooks/01_data_exploration.ipynb` - Exploratory data analysis
- `notebooks/02_feature_engineering.ipynb` - Feature creation and selection
- `notebooks/03_model_training.ipynb` - Neural network training
- `notebooks/04_explainability.ipynb` - SHAP analysis and interpretation

## Requirements

```
tensorflow>=2.8.0
scikit-learn>=1.0.0
shap>=0.40.0
pandas>=1.3.0
matplotlib>=3.4.0
jupyter>=1.0.0
```

## Citation

```bibtex
@article{garcia2023explainable,
  title={Explainable Neural Networks for Credit Risk Assessment},
  author={Garcia, Maria and Chen, Robert},
  journal={SSRN Electronic Journal},
  year={2023},
  doi={10.2139/ssrn.3456789}
}
```

## Replication

To replicate our results:

1. Install dependencies: `pip install -r requirements.txt`
2. Run notebooks in order: `jupyter notebook`
3. Train model: `python train.py`
4. Generate predictions: `python predict.py`
""",
    },
    {
        "name": "market-microstructure",
        "description": "High-frequency trading analysis and market microstructure research",
        "topics": ["high-frequency-trading", "market-microstructure", "time-series", "finance"],
        "readme": """# Market Microstructure Analysis

Code repository for "Price Discovery in High-Frequency Markets" (Journal of Finance, 2024).

## Authors

- David Lee (Quantitative Finance Department)
- Sarah Williams (Trading Systems Lab)

## Abstract

We analyze price discovery mechanisms in high-frequency trading environments using millisecond-level order book data from major exchanges.

## Published Papers

- **Main Paper**: DOI: 10.1111/jofi.2024.12345
- **Working Paper**: arXiv:2201.67890

## Data

- `data/orderbook/` - Limit order book snapshots (10ms frequency)
- `data/trades/` - Trade and quote data
- Total size: ~50GB (available via Zenodo: 10.5281/zenodo.1234567)

## Code Structure

```
src/
  orderbook.py - Order book reconstruction
  metrics.py - Microstructure metrics
  analysis.py - Statistical analysis
notebooks/
  analysis.ipynb - Main analysis notebook
tests/
  test_orderbook.py - Unit tests
```

## Requirements

```
numpy>=1.21.0
pandas>=1.3.0
numba>=0.55.0
pytest>=6.2.0
```

## Docker

For reproducibility, we provide a Docker environment:

```bash
docker build -t market-microstructure .
docker run -v $(pwd)/data:/data market-microstructure python src/analysis.py
```

## Citation

```bibtex
@article{lee2024price,
  title={Price Discovery in High-Frequency Markets},
  author={Lee, David and Williams, Sarah},
  journal={Journal of Finance},
  year={2024},
  doi={10.1111/jofi.2024.12345}
}
```

## References

This work cites and extends:
- Hasbrouck (1991) - Measuring the information content of stock trades
- Biais et al. (1995) - An empirical analysis of the limit order book
""",
    },
]


def create_repositories(org_name, token):
    """Create example research repositories."""
    print("=" * 60)
    print("Creating Example Research Repositories")
    print("=" * 60)

    g = Github(token)
    org = g.get_organization(org_name)

    print(f"\nOrganization: {org_name}")
    print(f"Creating {len(EXAMPLE_REPOS)} example repositories...\n")

    created = []
    errors = []

    for repo_config in EXAMPLE_REPOS:
        repo_name = repo_config["name"]
        print(f"Creating: {repo_name}...")

        try:
            # Check if repo already exists
            try:
                repo = org.get_repo(repo_name)
                print(f"  Repository exists: {repo.html_url}")
            except:
                # Create repository
                repo = org.create_repo(
                    name=repo_name,
                    description=repo_config["description"],
                    private=False,
                    has_issues=True,
                    has_wiki=False,
                    has_downloads=True,
                    auto_init=True,
                )
                print(f"  Created: {repo.html_url}")

            # Add topics
            repo.replace_topics(repo_config["topics"])
            print(f"  Added topics: {', '.join(repo_config['topics'])}")

            # Update README (get existing file first)
            try:
                readme = repo.get_contents("README.md")
                repo.update_file(
                    path="README.md",
                    message="Add research README",
                    content=repo_config["readme"],
                    sha=readme.sha,
                )
                print("  Updated README.md")
            except:
                repo.create_file(
                    path="README.md", message="Add research README", content=repo_config["readme"]
                )
                print("  Created README.md")

            # Create requirements.txt based on README content
            requirements = []
            for line in repo_config["readme"].split("\n"):
                if ">=" in line and not line.strip().startswith("#"):
                    req = line.strip().replace("```", "")
                    if req:
                        requirements.append(req)

            if requirements:
                repo.create_file(
                    path="requirements.txt",
                    message="Add requirements",
                    content="\n".join(requirements),
                )
                print(f"  Added requirements.txt ({len(requirements)} dependencies)")

            created.append(repo_name)
            print("  Success!\n")

        except Exception as e:
            print(f"  Error: {str(e)}\n")
            errors.append(f"{repo_name}: {str(e)}")

    print("=" * 60)
    print(f"Created {len(created)}/{len(EXAMPLE_REPOS)} repositories")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    print("=" * 60)

    return created, errors


def main():
    """Main execution."""
    # Get credentials
    token = os.environ.get("GITHUB_TOKEN")
    if not token and len(sys.argv) > 2:
        token = sys.argv[2]

    if not token:
        print("Error: GitHub token required")
        print("Usage: python create_example_repos.py <org_name> [token]")
        print("Or set GITHUB_TOKEN environment variable")
        sys.exit(1)

    org_name = sys.argv[1] if len(sys.argv) > 1 else "Digital-AI-Finance"

    created, errors = create_repositories(org_name, token)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
