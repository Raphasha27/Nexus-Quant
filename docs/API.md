# Nexus-Quant API — Documentation

> Autonomous market anomaly detection and quantitative trading signal engine.

## Base URL

```
http://localhost:8000
```

## Overview

Nexus-Quant provides quantitative analysis tools:

- **Trading Signals** — BUY/SELL/HOLD signals with SMA and RSI indicators
- **Anomaly Detection** — Volume/price anomaly detection via z-score analysis
- **OHLCV Data** — Historical candlestick data for any ticker
- **Portfolio Optimization** — Mean-variance optimization with Sharpe ratio
- **Market Summary** — Sector performance and sentiment overview

---

## Endpoints

### Health & Info

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Platform status and available modes |
| `GET` | `/health` | Health check |

### Signal

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/signal` | Generate trading signal with indicators |

### Anomaly

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/anomaly` | Detect volume/price anomalies |

### OHLCV

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/ohlcv/{ticker}` | Get historical candlestick data |

### Portfolio

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/portfolio/optimize` | Optimize portfolio allocation |

### Market

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/market/summary` | Market sentiment and sector performance |

---

## Example Requests

### Generate Trading Signal

```bash
curl -X POST http://localhost:8000/api/v1/signal \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NQ-SYNTH",
    "strategy": "momentum",
    "risk_tolerance": 0.7
  }'
```

**Response:**
```json
{
  "ticker": "NQ-SYNTH",
  "strategy": "momentum",
  "signal": "BUY",
  "confidence": 0.842,
  "indicators": {
    "sma_5": 152.30,
    "sma_20": 149.85,
    "rsi": 42.15
  },
  "generated_at": "2025-01-15T10:30:00"
}
```

### Detect Anomalies

```bash
curl -X POST http://localhost:8000/api/v1/anomaly \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NQ-SYNTH",
    "lookback_days": 30
  }'
```

**Response:**
```json
{
  "ticker": "NQ-SYNTH",
  "lookback_days": 30,
  "anomalies_detected": 2,
  "anomalies": [
    {
      "date": "2025-01-10",
      "volume": 4850000,
      "z_score": 2.15
    }
  ],
  "avg_volume": 2500000,
  "alert": false
}
```

### Get OHLCV Data

```bash
curl "http://localhost:8000/api/v1/ohlcv/NQ-SYNTH?days=14"
```

**Response:**
```json
{
  "ticker": "NQ-SYNTH",
  "data": [
    {
      "date": "2025-01-14",
      "open": 150.25,
      "high": 153.80,
      "low": 148.90,
      "close": 152.10,
      "volume": 2500000
    }
  ]
}
```

### Optimize Portfolio

```bash
curl -X POST http://localhost:8000/api/v1/portfolio/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["NQ-A", "NQ-B", "NQ-C"],
    "capital": 100000.00
  }'
```

**Response:**
```json
{
  "strategy": "mean_variance_optimization",
  "total_capital": 100000.00,
  "expected_return": 0.1425,
  "sharpe_ratio": 1.85,
  "max_drawdown": 0.095,
  "allocations": {
    "NQ-A": {"weight": 0.3520, "capital_usd": 35200.00},
    "NQ-B": {"weight": 0.4180, "capital_usd": 41800.00},
    "NQ-C": {"weight": 0.2300, "capital_usd": 23000.00}
  }
}
```

### Market Summary

```bash
curl http://localhost:8000/api/v1/market/summary
```

**Response:**
```json
{
  "timestamp": "2025-01-15T10:30:00",
  "market_sentiment": "Bullish",
  "vix": 18.45,
  "sector_performance": {
    "Technology": 2.35,
    "Finance": 1.10,
    "Healthcare": -0.45,
    "Energy": 3.20,
    "Consumer": 0.85
  }
}
```

---

## Interactive Docs

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec:** [`docs/api-spec.yaml`](./api-spec.yaml)
