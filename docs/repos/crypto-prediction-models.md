# crypto-prediction-models

Deep learning models for cryptocurrency price prediction and volatility forecasting

[View on GitHub](https://github.com/Digital-AI-Finance/crypto-prediction-models){ .md-button .md-button--primary }


---

## Information

| Property | Value |
|----------|-------|
| Language | Python |
| Stars | 512 |
| Forks | 145 |
| Watchers | 67 |
| Open Issues | 22 |
| License | MIT License |
| Created | 2023-04-12 |
| Last Updated | 2025-01-20 |
| Last Push | 2025-01-20 |
| Contributors | 15 |
| Default Branch | main |
| Visibility | public |


## Topics

`cryptocurrency` `deep-learning` `prediction` `lstm` `transformers` 



## Latest Release

- Version: v2.5.0
- Name: Transformer Models
- Published: 2024-12-20


## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Enabled

## README

# Crypto Prediction Models

State-of-the-art deep learning models for cryptocurrency price prediction and volatility forecasting.

## Models

- LSTM networks for time series
- Transformer-based architectures
- GRU with attention mechanisms
- Ensemble methods
- Hybrid CNN-LSTM models

## Features

- Multi-crypto support (BTC, ETH, and 100+ altcoins)
- Real-time price feeds
- On-chain data integration
- Social sentiment incorporation
- Volatility predictions
- Risk metrics

## Performance

- Bitcoin: 72% directional accuracy (7-day)
- Ethereum: 68% directional accuracy (7-day)
- Volatility RMSE: 0.15 (normalized)

## Quick Start

```python
from crypto_prediction import CryptoPredictor

predictor = CryptoPredictor('BTC')
forecast = predictor.predict(days=7)
```