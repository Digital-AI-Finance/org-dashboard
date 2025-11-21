# backtesting-framework

High-performance backtesting framework for trading strategies with realistic market simulation

[View on GitHub](https://github.com/Digital-AI-Finance/backtesting-framework){ .md-button .md-button--primary }


---

## Information

| Property | Value |
|----------|-------|
| Language | Python |
| Stars | 387 |
| Forks | 91 |
| Watchers | 48 |
| Open Issues | 14 |
| License | MIT License |
| Created | 2023-07-15 |
| Last Updated | 2025-01-19 |
| Last Push | 2025-01-19 |
| Contributors | 10 |
| Default Branch | main |
| Visibility | public |


## Topics

`backtesting` `trading` `simulation` `quantitative-finance` 



## Latest Release

- Version: v1.9.0
- Name: Options Support
- Published: 2024-11-25


## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Disabled

## README

# Backtesting Framework

A high-performance, event-driven backtesting framework for trading strategies with realistic market simulation.

## Features

- Event-driven architecture
- Realistic order execution simulation
- Transaction cost modeling
- Slippage and market impact
- Multiple asset classes (stocks, futures, options, crypto)
- Portfolio-level backtesting
- Risk analytics and reporting
- Parallel processing support

## Performance

- Backtest 10 years of daily data: < 2 seconds
- Minute-level data: < 30 seconds
- Supports multi-asset portfolios (1000+ securities)

## Example

```python
from backtesting import Backtest, Strategy

class MyStrategy(Strategy):
    def init(self):
        pass
        
    def next(self):
        if self.data.Close[-1] > self.data.Close[-2]:
            self.buy()

bt = Backtest(data, MyStrategy)
results = bt.run()
bt.plot()
```