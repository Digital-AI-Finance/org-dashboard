# financial-data-api

RESTful API for accessing financial market data, fundamental data, and alternative data sources

[View on GitHub](https://github.com/Digital-AI-Finance/financial-data-api){ .md-button .md-button--primary }
[Homepage](https://api.digital-ai-finance.com){ .md-button }

---

## Information

| Property | Value |
|----------|-------|
| Language | TypeScript |
| Stars | 198 |
| Forks | 41 |
| Watchers | 28 |
| Open Issues | 6 |
| License | Apache License 2.0 |
| Created | 2023-07-20 |
| Last Updated | 2025-01-17 |
| Last Push | 2025-01-17 |
| Contributors | 7 |
| Default Branch | main |
| Visibility | public |


## Topics

`api` `finance` `market-data` `nodejs` `express` 



## Latest Release

- Version: v1.4.0
- Name: WebSocket Support
- Published: 2024-12-10


## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Disabled

## README

# Financial Data API

A comprehensive RESTful API providing access to financial market data, fundamental data, and alternative data sources.

## Endpoints

- `/api/v1/stocks/{symbol}` - Stock quotes and historical data
- `/api/v1/fundamentals/{symbol}` - Financial statements and ratios
- `/api/v1/news` - Financial news aggregation
- `/api/v1/crypto` - Cryptocurrency data
- `/api/v1/sentiment` - Market sentiment indicators

## Features

- Real-time and historical data
- Rate limiting and authentication
- WebSocket support for streaming
- Comprehensive documentation (OpenAPI)
- Client SDKs (Python, JavaScript, R)

## Quick Start

```bash
curl https://api.digital-ai-finance.com/api/v1/stocks/AAPL
```

## Authentication

API key required. Register at https://digital-ai-finance.com/api-keys