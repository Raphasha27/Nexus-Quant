# Nexus Quant — Architecture

## System Overview

Nexus Quant is a quantitative trading analytics and signal generation engine built with FastAPI. It provides real-time market data processing, 15+ technical indicators, ML-powered anomaly detection, portfolio optimisation, and a backtesting framework through a clean REST API. All data is synthetically generated for simulation and prototyping.

## Architecture Diagram

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
│  │ │ Backtest│ │ │
│  │ └────────┘ │ │
│  └─────┬──────┘ │
└────────┼────────┘
         │
    ┌────▼────────────┐
    │  Synthetic Data  │
    │  Generator       │
    │  (OHLCV + News)  │
    └─────────────────┘
```

## Technology Stack

| Component         | Technology        | Version |
|-------------------|-------------------|---------|
| Language          | Python            | 3.11+   |
| Framework         | FastAPI           | —       |
| Data Processing   | pandas, NumPy     | —       |
| Machine Learning  | scikit-learn      | —       |
| Validation        | Pydantic          | —       |
| Testing           | pytest            | —       |
| Linting           | ruff              | —       |
| Container         | Docker            | —       |
| Deployment        | Vercel            | —       |

## Directory Structure

```
Nexus-Quant/
├── api/
│   ├── main.py            # FastAPI application with quant engine
│   └── index.py           # Vercel serverless entrypoint
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── index.html             # Static frontend
├── data.csv               # Sample market data
├── Dockerfile             # Container build
├── .dockerignore          # Docker build exclusions
├── vercel.json            # Vercel deployment config
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

## Data Flow

### Signal Generation
1. Client sends `POST /api/v1/signal` with ticker, strategy, and risk tolerance.
2. System generates synthetic OHLCV data for the ticker.
3. Technical indicators computed: SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic, Williams %R, CCI, OBV, VWAP, Ichimoku.
4. Momentum-based signal engine combines indicators with multi-confirmation logic.
5. Returns BUY/SELL/HOLD signal with confidence score and indicator breakdown.

### Anomaly Detection
1. Client sends `POST /api/v1/anomaly` with ticker and volume data.
2. Z-score statistical analysis applied to volume series.
3. Anomalies flagged where |z-score| > threshold.
4. Returns anomaly points with severity classification.

### Portfolio Optimisation
1. Client sends `POST /api/v1/portfolio/optimize` with asset weights and returns.
2. Mean-variance optimization (Markowitz) computes efficient frontier.
3. Returns optimal weights, Sharpe ratio, and max drawdown.

### Market Intelligence
1. `GET /api/v1/market/summary` returns market sentiment.
2. Sector performance tracking across technology, healthcare, finance, energy.
3. Real-time sentiment scoring from synthetic news feed.

### Backtesting
1. `GET /api/v1/ohlcv/{ticker}` returns historical OHLCV data.
2. Synthetic data generator creates realistic price movements.
3. Strategy validation against historical data.

## Security

- **No real financial data**: All data is synthetic; no live market connections.
- **No authentication by default**: Add API key auth for production.
- **Input validation**: Pydantic models validate all numeric inputs.
- **Environment variables**: Configuration loaded from `.env` file.

## Deployment

### Docker

```bash
docker build -t nexus-quant .
docker run -p 8000:8000 nexus-quant
```

### Vercel (Serverless)

```bash
vercel deploy
```

### Local Development

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### API Endpoints

| Method | Path                        | Description                          |
|--------|-----------------------------|--------------------------------------|
| GET    | `/`                         | API status and available modes       |
| GET    | `/health`                   | System health check                  |
| POST   | `/api/v1/signal`            | Generate trading signal              |
| POST   | `/api/v1/anomaly`           | Detect volume anomalies             |
| GET    | `/api/v1/ohlcv/{ticker}`    | Get OHLCV market data               |
| POST   | `/api/v1/portfolio/optimize`| Portfolio optimisation               |
| GET    | `/api/v1/market/summary`    | Market sentiment and sector performance |

## Scaling Considerations

- **Data persistence**: Replace in-memory store with TimescaleDB for time-series data.
- **Real-time streaming**: Kafka/WebSocket for live market data ingestion.
- **GPU acceleration**: cuML for GPU-accelerated ML anomaly detection.
- **Batch processing**: Celery workers for large-scale backtesting across tickers.
- **Caching**: Redis for frequently accessed indicator calculations.
- **Multi-asset**: Extend to forex, crypto, commodities with asset-specific models.

## Decision Records

| Decision | Rationale |
|----------|-----------|
| Synthetic data | No market data licensing; demonstrates capabilities without regulatory concerns |
| FastAPI | Async support for concurrent calculations; auto-generated API docs |
| scikit-learn | Mature ML library; sufficient for statistical anomaly detection |
| In-memory store | Zero-config for demo; fast iteration without database setup |
| Vercel serverless | Scales to zero; cost-effective for demo/prototyping |
| 15+ indicators | Comprehensive indicator set demonstrates technical analysis breadth |
| Markowitz optimization | Industry-standard portfolio theory; well-understood mathematical foundation |
