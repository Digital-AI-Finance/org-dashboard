# sentiment-analysis-finance

NLP-based sentiment analysis for financial news and social media to predict market movements

[View on GitHub](https://github.com/Digital-AI-Finance/sentiment-analysis-finance){ .md-button .md-button--primary }


---

## Information

| Property | Value |
|----------|-------|
| Language | Python |
| Stars | 425 |
| Forks | 103 |
| Watchers | 52 |
| Open Issues | 18 |
| License | MIT License |
| Created | 2023-05-08 |
| Last Updated | 2025-01-21 |
| Last Push | 2025-01-21 |
| Contributors | 12 |
| Default Branch | main |
| Visibility | public |


## Topics

`nlp` `sentiment-analysis` `finance` `deep-learning` `transformers` 



## Latest Release

- Version: v3.2.0
- Name: GPT Integration
- Published: 2025-01-05


## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Enabled

## README

# Sentiment Analysis for Finance

Advanced NLP-based sentiment analysis specifically designed for financial news, earnings calls, and social media to predict market movements.

## Features

- Financial-domain BERT models
- Real-time news scraping
- Twitter sentiment tracking
- Earnings call analysis
- Multi-source sentiment aggregation
- Market impact prediction

## Supported Sources

- Reuters, Bloomberg, WSJ
- Twitter/X financial discussions
- Reddit (r/wallstreetbets, r/investing)
- Company earnings transcripts
- SEC filings (10-K, 10-Q)

## Usage

```python
from sentiment_finance import SentimentAnalyzer

analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze_stock('AAPL')
```