# portfolio-optimization-ml

Machine learning approaches to portfolio optimization using deep reinforcement learning

[View on GitHub](https://github.com/Digital-AI-Finance/portfolio-optimization-ml){ .md-button .md-button--primary }


---




## Publications


### Financial markets and unemployment



| Property | Value |
|----------|-------|
| DOI | [10.1016/j.jfineco.2023.01.001](https://doi.org/10.1016/j.jfineco.2023.01.001) |


| Year | 2023 |
| Venue | Journal of Financial Economics |
| Citations | 16 |


**Authors**: Tommaso Monacelli, Vincenzo Quadrini, Antonella Trigari


---

### Publication 2



| Property | Value |
|----------|-------|

| arXiv | [2103.12345](https://arxiv.org/abs/2103.12345) |







---



## Information

| Property | Value |
|----------|-------|
| Language | Unknown |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-11-21 |
| Last Updated | 2025-11-21 |
| Last Push | 2025-11-21 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | public |


## Topics

`finance` `machine-learning` `portfolio-optimization` `reinforcement-learning` 







## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# Portfolio Optimization with Deep Reinforcement Learning

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
