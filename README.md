<div align="center">

# Nexus Quant

**Quantitative Trading Analytics & Signal Generation Engine with ML-Powered Anomaly Detection**

[![CI](https://github.com/Raphasha27/Nexus-Quant/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/Nexus-Quant/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-4B2E83)](https://docs.astral.sh/ruff/)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-91%25-brightgreen)](https://github.com/Raphasha27/Nexus-Quant)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)](https://github.com/Raphasha27/Nexus-Quant)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)

</div>

---

## Features

- **15+ Technical Indicators** — SMA, EMA, RSI, MACD, Bollinger Bands, and more
- **ML Anomaly Detection** — Volume-based z-score statistical analysis
- **Trading Signal Generation** — Momentum-based engine with multi-indicator confirmation
- **Portfolio Optimisation** — Mean-variance optimization with Sharpe ratio & max drawdown
- **Backtesting Framework** — Synthetic OHLCV data generation for strategy validation
- **Market Sentiment** — Real-time sentiment analysis with sector performance tracking
- **REST API** — Comprehensive API with automatic OpenAPI documentation at `/docs`

---

## Quick Start

```bash
git clone https://github.com/Raphasha27/Nexus-Quant.git
cd Nexus-Quant
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

API docs (Swagger UI): `http://localhost:8000/docs`

### Docker

```bash
docker build -t nexus-quant .
docker run -p 8000:8000 nexus-quant
```

---

## Architecture

> Full architecture documentation: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

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

## API Documentation

> Full API reference: [docs/API.md](docs/API.md) · Swagger UI: `http://localhost:8000/docs`

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

| Component | Technology | Description |
|-----------|------------|-------------|
| Language | Python 3.11+ | Core runtime |
| Framework | FastAPI | Async REST API |
| Data Processing | pandas, numpy | Financial data manipulation |
| Machine Learning | scikit-learn | Anomaly detection models |
| Validation | Pydantic | Request/response schemas |
| Testing | pytest | Unit and integration tests |
| Linting | ruff | Fast Python linter |
| Container | Docker | Single-container deployment |

---

## Project Structure

```
Nexus-Quant/
├── api/
│   └── main.py           # FastAPI application with quant engine
├── tests/                # Unit tests
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
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
├── LICENSE
└── README.md
```

---

## Testing

```bash
pip install -e ".[dev]"
pytest --cov=api --cov-report=term-missing -v
ruff check api/
ruff format api/ --check
```

---

## Deployment

### Docker

```bash
docker build -t nexus-quant .
docker run -d -p 8000:8000 --name nexus-quant nexus-quant
docker logs nexus-quant     # View logs
docker stop nexus-quant      # Stop container
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PORT` | `8000` | FastAPI server port |
| `LOG_LEVEL` | `info` | Logging verbosity |
| `DATA_SOURCE` | `synthetic` | Market data source |
| `ANOMALY_THRESHOLD` | `2.0` | Z-score threshold for anomalies |

### Local Development

```bash
pip install -e ".[dev]"
uvicorn api.main:app --reload --port 8000
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Part of the <a href="https://github.com/Raphasha27">Kirov Dynamics Technology</a> portfolio
</div>
