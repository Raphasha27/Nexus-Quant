<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffcc,100:004a99&height=200&section=header&text=Nexus-Quant&fontSize=50&fontColor=ffffff&fontAlignY=40&desc=Quantitative%20Trading%20%26%20Market%20Analytics%20Engine&descAlignY=65" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white&style=for-the-badge)](https://fastapi.tiangolo.com)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)](https://docker.com)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
</div>

## Overview

Nexus-Quant is a quantitative trading and market analytics engine built with FastAPI. It provides real-time market data processing, technical analysis indicators, portfolio risk assessment, and backtesting capabilities through a clean REST API.

## Features

- **Trading Signal Generation** — Momentum-based signal engine with SMA crossover + RSI confirmation
- **Anomaly Detection** — Volume-based anomaly scoring with z-score statistical analysis
- **Portfolio Optimization** — Mean-variance optimization with allocation and risk metrics
- **Market Data** — Synthetic OHLCV data generation for backtesting and simulation
- **Market Sentiment** — Real-time sentiment analysis with sector performance tracking
- **REST API** — Comprehensive API with automatic OpenAPI documentation

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

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API status and available modes |
| GET | `/health` | System health check |
| POST | `/api/v1/signal` | Generate trading signal for a ticker |
| POST | `/api/v1/anomaly` | Detect volume anomalies |
| GET | `/api/v1/ohlcv/{ticker}` | Get OHLCV market data |
| POST | `/api/v1/portfolio/optimize` | Run portfolio optimization |
| GET | `/api/v1/market/summary` | Market sentiment and sector performance |
| GET | `/docs` | Swagger documentation |

## Project Structure

```
Nexus-Quant/
├── api/
│   └── main.py          # FastAPI application with quant engine
├── requirements.txt     # Dependencies
├── Dockerfile           # Container build
└── .env.example         # Environment template
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

© 2026 **Kirov Dynamics Technology** | Built by **Koketso Raphasha (Raphasha27)**
