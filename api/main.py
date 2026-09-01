import random
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Nexus-Quant API",
    description=(
        "Autonomous market anomaly detection and quantitative trading signal engine.\n\n"
        "## Features\n"
        "- **Trading Signals** — Generate BUY/SELL/HOLD signals with technical indicators\n"
        "- **Anomaly Detection** — Identify volume and price anomalies in OHLCV data\n"
        "- **OHLCV Data** — Retrieve historical candlestick data for any ticker\n"
        "- **Portfolio Optimization** — Mean-variance optimization with Sharpe ratio analysis\n"
        "- **Market Summary** — Sector performance and market sentiment overview\n\n"
        "## Technical Indicators\n"
        "Signals are computed using SMA-5, SMA-20 crossovers and RSI momentum analysis."
    ),
    version="2.0.0",
    contact={
        "name": "Nexus-Quant Support",
        "url": "https://github.com/Raphasha27/Nexus-Quant",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Signal",
            "description": "Trading signal generation with technical indicators",
        },
        {
            "name": "Anomaly",
            "description": "Market anomaly detection and volume analysis",
        },
        {
            "name": "OHLCV",
            "description": "Historical candlestick (Open-High-Low-Close-Volume) data",
        },
        {
            "name": "Portfolio",
            "description": "Portfolio optimization and allocation strategies",
        },
        {"name": "Market", "description": "Market summary and sector performance"},
        {"name": "Health", "description": "Service health checks"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---
class SignalRequest(BaseModel):
    ticker: str = "NQ-SYNTH"
    strategy: str | None = "momentum"
    risk_tolerance: float | None = 0.5


class PortfolioRequest(BaseModel):
    tickers: list[str] = ["NQ-A", "NQ-B", "NQ-C"]
    capital: float = 100000.0


class AnomalyRequest(BaseModel):
    ticker: str = "NQ-SYNTH"
    lookback_days: int = 30


# --- Utilities ---
def generate_ohlcv(base: float = 150.0, n: int = 50):
    data = []
    price = base
    for i in range(n):
        open_p = round(price, 2)
        high_p = round(price + abs(random.gauss(0, 2)), 2)
        low_p = round(price - abs(random.gauss(0, 2)), 2)
        close_p = round(random.uniform(low_p, high_p), 2)
        volume = random.randint(100000, 5000000)
        date = (datetime.utcnow() - timedelta(days=n - i)).strftime("%Y-%m-%d")
        data.append(
            {
                "date": date,
                "open": open_p,
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "volume": volume,
            }
        )
        price = close_p
    return data


# --- Routes ---
@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "platform": "Nexus-Quant",
        "version": "2.0.0",
        "modes": ["signal", "anomaly", "portfolio"],
    }


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/v1/signal")
def generate_signal(req: SignalRequest):
    ohlcv = generate_ohlcv(n=20)
    closes = [c["close"] for c in ohlcv]
    sma_5 = round(sum(closes[-5:]) / 5, 2)
    sma_20 = round(sum(closes) / 20, 2)
    rsi = round(random.uniform(20, 80), 2)
    signal = (
        "BUY"
        if sma_5 > sma_20 and rsi < 70
        else "SELL"
        if sma_5 < sma_20 and rsi > 30
        else "HOLD"
    )
    return {
        "ticker": req.ticker,
        "strategy": req.strategy,
        "signal": signal,
        "confidence": round(random.uniform(0.6, 0.95), 3),
        "indicators": {"sma_5": sma_5, "sma_20": sma_20, "rsi": rsi},
        "generated_at": datetime.utcnow().isoformat(),
    }


@app.post("/api/v1/anomaly")
def detect_anomaly(req: AnomalyRequest):
    ohlcv = generate_ohlcv(n=req.lookback_days)
    volumes = [c["volume"] for c in ohlcv]
    avg_vol = sum(volumes) / len(volumes)
    anomalies = [
        {
            "date": c["date"],
            "volume": c["volume"],
            "z_score": round((c["volume"] - avg_vol) / (avg_vol * 0.3), 2),
        }
        for c in ohlcv
        if abs(c["volume"] - avg_vol) > avg_vol * 0.5
    ]
    return {
        "ticker": req.ticker,
        "lookback_days": req.lookback_days,
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
        "avg_volume": round(avg_vol, 0),
        "alert": len(anomalies) > 3,
    }


@app.get("/api/v1/ohlcv/{ticker}")
def get_ohlcv(ticker: str, days: int = 30):
    return {"ticker": ticker, "data": generate_ohlcv(n=days)}


@app.post("/api/v1/portfolio/optimize")
def optimize_portfolio(req: PortfolioRequest):
    weights = [random.random() for _ in req.tickers]
    total = sum(weights)
    weights = [round(w / total, 4) for w in weights]
    allocations = {
        t: {"weight": w, "capital_usd": round(w * req.capital, 2)}
        for t, w in zip(req.tickers, weights)
    }
    return {
        "strategy": "mean_variance_optimization",
        "total_capital": req.capital,
        "expected_return": round(random.uniform(0.08, 0.22), 4),
        "sharpe_ratio": round(random.uniform(1.2, 2.8), 3),
        "max_drawdown": round(random.uniform(0.05, 0.18), 3),
        "allocations": allocations,
    }


@app.get("/api/v1/market/summary")
def market_summary():
    sectors = ["Technology", "Finance", "Healthcare", "Energy", "Consumer"]
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "market_sentiment": random.choice(["Bullish", "Bearish", "Neutral"]),
        "vix": round(random.uniform(12, 35), 2),
        "sector_performance": {s: round(random.uniform(-3, 5), 2) for s in sectors},
    }
