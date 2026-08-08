<div align="center">
  <a href="https://raphasha27.github.io/Nexus-Quant/">
    <img src="https://img.shields.io/badge/LIVE_DEPLOYMENT-View_App-0EA5E9?style=for-the-badge&logo=github&logoColor=white" alt="Live Deployment" />
  </a>
</div>

<br/>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffcc,100:004a99&height=200&section=header&text=Nexus-Quant&fontSize=50&fontColor=ffffff&fontAlignY=40&desc=Quantitative%20Trading%20%26%20Market%20Analytics%20Engine&descAlignY=65" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white&style=for-the-badge)](https://fastapi.tiangolo.com)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)](https://docker.com)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
  [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=for-the-badge)](https://github.com/astral-sh/ruff)
</div>

## Overview

Nexus-Quant is a quantitative trading and market analytics engine built with FastAPI. It provides real-time market data processing, technical analysis indicators, portfolio risk assessment, and backtesting capabilities through a clean REST API. All data is synthetically generated for simulation and prototyping.

## Features

- **Trading Signal Generation** — Momentum-based signal engine with SMA crossover + RSI confirmation
- **Anomaly Detection** — Volume-based anomaly scoring with z-score statistical analysis
- **Portfolio Optimization** — Mean-variance optimization with allocation and risk metrics (Sharpe ratio, max drawdown)
- **Market Data** — Synthetic OHLCV data generation for backtesting and simulation
- **Market Sentiment** — Real-time sentiment analysis with sector performance tracking
- **REST API** — Comprehensive API with automatic OpenAPI documentation at `/docs`

## Quick Start

```bash
git clone https://github.com/Raphasha27/Nexus-Quant.git
cd Nexus-Quant
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

Or with Docker:

```bash
docker build -t nexus-quant .
docker run -p 8000:8000 nexus-quant
```

## API Endpoints

### System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API status and available modes |
| GET | `/health` | System health check |

### Trading Signals

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/signal` | Generate trading signal for a ticker |

**POST `/api/v1/signal`**

```json
{
  "ticker": "NQ-SYNTH",
  "strategy": "momentum",
  "risk_tolerance": 0.5
}
```

Response:
```json
{
  "ticker": "NQ-SYNTH",
  "signal": "BUY",
  "confidence": 0.873,
  "indicators": { "sma_5": 152.34, "sma_20": 148.12, "rsi": 62.45 }
}
```

### Anomaly Detection

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/anomaly` | Detect volume anomalies |

### Market Data

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/ohlcv/{ticker}` | Get OHLCV market data |

### Portfolio Management

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/portfolio/optimize` | Run portfolio optimization |

### Market Intelligence

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/market/summary` | Market sentiment and sector performance |

## Project Structure

```
Nexus-Quant/
├── api/
│   └── main.py           # FastAPI application with quant engine
├── tests/                # Unit tests
├── Dockerfile            # Container build
├── .dockerignore         # Docker build exclusions
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata and build config
└── .pre-commit-config.yaml
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check api/
ruff format api/ --check
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Ecosystem

Part of the **Kirov Dynamics Technology** ecosystem:

[![Portfolio](https://img.shields.io/badge/Portfolio-⭐29-00ffcc?style=flat-square)](https://github.com/Raphasha27/Portfolio)
[![AI-Agent](https://img.shields.io/badge/AI--Agent-⭐3-004a99?style=flat-square)](https://github.com/Raphasha27/AI-Agent)
[![Nexus-Quant](https://img.shields.io/badge/Nexus--Quant-Quant-00ffcc?style=flat-square)](https://github.com/Raphasha27/Nexus-Quant)
[![Repo Audit](https://img.shields.io/badge/Repo--Audit--Bot-CLI-00ffcc?style=flat-square)](https://github.com/Raphasha27/repo-audit-bot)

*Building the infrastructure of autonomous systems.*

<br/>

---

<h3 align="center">🐍 Part of the <a href="https://github.com/Raphasha27">Raphasha27</a> Ecosystem</h3>

<p align="center">
  <a href="https://github.com/Raphasha27/Raphasha27">
    <img src="https://img.shields.io/badge/Back_to_Profile-0D1117?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://raphasha27.github.io/Raphasha27/ai-snake-game/">
    <img src="https://img.shields.io/badge/▶_Play_AI_Snake-0EA5E9?style=for-the-badge&logo=javascript&logoColor=white" />
  </a>
</p>

---

© 2026 **Kirov Dynamics Technology** | Built by **Koketso Raphasha (Raphasha27)**
