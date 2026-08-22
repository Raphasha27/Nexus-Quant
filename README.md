# Nexus Quant

### Quantitative Trading Analytics & Signal Generation Engine

<div align="center">

[![CI](https://github.com/Raphasha27/Nexus-Quant/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/Nexus-Quant/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-a78bfa?style=flat-square)

</div>

---

## Overview

Nexus Quant is a **quantitative trading analytics and signal generation engine** built with FastAPI. It provides real-time market data processing, 15+ technical indicators, ML-powered anomaly detection, portfolio optimisation, and a backtesting framework through a clean REST API. All data is synthetically generated for simulation and prototyping.

> Built for quantitative research — not financial advice.

---

## Features

- [x] 15+ Technical Indicators — SMA, EMA, RSI, MACD, Bollinger Bands, and more
- [x] ML Anomaly Detection — Volume-based z-score statistical analysis
- [x] Trading Signal Generation — Momentum-based engine with multi-indicator confirmation
- [x] Portfolio Optimisation — Mean-variance optimization with Sharpe ratio & max drawdown
- [x] Backtesting Framework — Synthetic OHLCV data generation for strategy validation
- [x] Market Sentiment — Real-time sentiment analysis with sector performance tracking
- [x] REST API — Comprehensive API with automatic OpenAPI documentation at `/docs`

---

## Architecture

```
┌─────────────────┐
│  Dashboard UI   │
│  (Static/SPA)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   :8000         │
│  ┌────────────┐ │
│  │ Quant      │ │
│  │ Engine     │ │
│  │ ┌────────┐ │ │
│  │ │ Signal │ │ │
│  │ │ Anomaly│ │ │
│  │ │Portfolio│ │ │
│  │ └────────┘ │ │
│  └─────┬──────┘ │
└────────┼────────┘
         │
    ┌────▼────────────┐
    │  Synthetic Data  │
    │  Generator       │
    └─────────────────┘
```

---

## Quick Start

### Using pip + uvicorn

```bash
git clone https://github.com/Raphasha27/Nexus-Quant.git
cd Nexus-Quant
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### Using Docker

```bash
docker build -t nexus-quant .
docker run -p 8000:8000 nexus-quant
```

API docs available at `http://localhost:8000/docs`

---

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

```json
{
  "ticker": "NQ-SYNTH",
  "strategy": "momentum",
  "risk_tolerance": 0.5
}
```

### Anomaly Detection

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/anomaly` | Detect volume anomalies with z-score analysis |

### Market Data

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/ohlcv/{ticker}` | Get OHLCV market data for backtesting |

### Portfolio Management

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/portfolio/optimize` | Run mean-variance portfolio optimisation |

### Market Intelligence

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/market/summary` | Market sentiment and sector performance |

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Data Processing | pandas, numpy |
| Machine Learning | scikit-learn |
| Validation | Pydantic |
| Testing | pytest |
| Linting | ruff |
| Container | Docker |

---

## Project Structure

```
Nexus-Quant/
├── api/
│   └── main.py           # FastAPI application with quant engine
├── tests/                # Unit tests
├── docs/                 # Documentation
├── index.html            # Static frontend
├── data.csv              # Sample market data
├── Dockerfile            # Container build
├── .dockerignore         # Docker build exclusions
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata and build config
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

---

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check api/
ruff format api/ --check
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Part of the <a href="https://github.com/Raphasha27">Kirov Dynamics Technology</a> portfolio
</div>
