"""Nexus-Quant — Autonomous market anomaly detection and quantitative trading signal engine."""

import math
import random
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Nexus-Quant API",
    description="Autonomous market anomaly detection and quantitative trading signal engine.",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SignalRequest(BaseModel):
    """Request model for generating a trading signal."""

    ticker: str = Field(default="NQ-SYNTH", min_length=1, max_length=20)
    strategy: str = Field(default="momentum", pattern=r"^[a-z_]+$")
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0)


class PortfolioRequest(BaseModel):
    """Request model for portfolio optimization."""

    tickers: list[str] = Field(default=["NQ-A", "NQ-B", "NQ-C"], min_length=1)
    capital: float = Field(default=100000.0, gt=0)


class AnomalyRequest(BaseModel):
    """Request model for anomaly detection."""

    ticker: str = Field(default="NQ-SYNTH", min_length=1, max_length=20)
    lookback_days: int = Field(default=30, ge=1, le=365)


def generate_ohlcv(base: float = 150.0, n: int = 50) -> list[dict]:
    """Generate synthetic OHLCV market data.

    Produces n days of synthetic open-high-low-close-volume data
    using a random walk starting from the given base price.

    Args:
        base: Starting price.
        n: Number of data points to generate.

    Returns:
        List of OHLCV dicts with date, open, high, low, close, volume.
    """
    data: list[dict] = []
    price = base
    for i in range(n):
        open_p = round(price, 2)
        high_p = round(price + abs(random.gauss(0, 2)), 2)
        low_p = round(price - abs(random.gauss(0, 2)), 2)
        close_p = round(random.uniform(low_p, high_p), 2)
        volume = random.randint(100000, 5000000)
        date = (datetime.now(timezone.utc) - timedelta(days=n - i)).strftime("%Y-%m-%d")
        data.append({
            "date": date,
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p,
            "volume": volume,
        })
        price = close_p
    return data


@app.get("/")
async def root() -> dict:
    """Root endpoint returning API status and available modes."""
    return {
        "status": "ONLINE",
        "platform": "Nexus-Quant",
        "version": app.version,
        "modes": ["signal", "anomaly", "portfolio"],
    }


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/api/v1/signal")
async def generate_signal(req: SignalRequest) -> dict:
    """Generate a trading signal based on SMA crossover and RSI confirmation.

    Computes 5-period and 20-period simple moving averages on synthetic
    OHLCV data, then combines with a simulated RSI to produce a
    BUY/SELL/HOLD signal.

    Args:
        req: Signal request with ticker, strategy, and risk tolerance.

    Returns:
        Trading signal with confidence score and technical indicators.
    """
    ohlcv = generate_ohlcv(n=20)
    closes = [c["close"] for c in ohlcv]
    sma_5 = round(sum(closes[-5:]) / 5, 2)
    sma_20 = round(sum(closes) / 20, 2)
    rsi = round(random.uniform(20, 80), 2)
    if sma_5 > sma_20 and rsi < 70:
        signal = "BUY"
    elif sma_5 < sma_20 and rsi > 30:
        signal = "SELL"
    else:
        signal = "HOLD"
    return {
        "ticker": req.ticker,
        "strategy": req.strategy,
        "signal": signal,
        "confidence": round(random.uniform(0.6, 0.95), 3),
        "indicators": {"sma_5": sma_5, "sma_20": sma_20, "rsi": rsi},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/v1/anomaly")
async def detect_anomaly(req: AnomalyRequest) -> dict:
    """Detect volume anomalies using z-score analysis.

    Compares each day's volume against the average volume; flags days
    where the absolute deviation exceeds 50% of the mean as anomalies.

    Args:
        req: Anomaly request with ticker and lookback period.

    Returns:
        Detection results including anomaly count, details, and alert flag.
    """
    ohlcv = generate_ohlcv(n=req.lookback_days)
    volumes = [c["volume"] for c in ohlcv]
    if not volumes:
        raise HTTPException(status_code=400, detail="No data available for anomaly detection")
    avg_vol = sum(volumes) / len(volumes)
    anomalies: list[dict] = [
        {
            "date": c["date"],
            "volume": c["volume"],
            "z_score": round((c["volume"] - avg_vol) / (avg_vol * 0.3 + 1), 2),
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
async def get_ohlcv(ticker: str, days: int = 30) -> dict:
    """Get synthetic OHLCV market data for a ticker.

    Args:
        ticker: The ticker symbol.
        days: Number of days of data to return (default 30, max 365).

    Returns:
        OHLCV data series for the requested ticker.
    """
    if not ticker or not ticker.strip():
        raise HTTPException(status_code=400, detail="ticker cannot be empty")
    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="days must be between 1 and 365")
    return {"ticker": ticker, "data": generate_ohlcv(n=days)}


@app.post("/api/v1/portfolio/optimize")
async def optimize_portfolio(req: PortfolioRequest) -> dict:
    """Run a mean-variance portfolio optimization simulation.

    Generates random weight allocations for the given tickers and computes
    simulated portfolio risk/return metrics.

    Args:
        req: Portfolio request with tickers and capital.

    Returns:
        Optimized portfolio with weight allocations, expected return,
        Sharpe ratio, and max drawdown.
    """
    if len(req.tickers) < 2:
        raise HTTPException(
            status_code=400, detail="At least two tickers are required for portfolio optimization"
        )
    weights = [random.random() for _ in req.tickers]
    total = sum(weights)
    weights = [round(w / total, 4) for w in weights]
    allocations: dict[str, dict] = {
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
async def market_summary() -> dict:
    """Get a synthetic market summary with sentiment and sector performance.

    Returns:
        Current market sentiment, VIX level, and sector performance data.
    """
    sectors = ["Technology", "Finance", "Healthcare", "Energy", "Consumer"]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "market_sentiment": random.choice(["Bullish", "Bearish", "Neutral"]),
        "vix": round(random.uniform(12, 35), 2),
        "sector_performance": {s: round(random.uniform(-3, 5), 2) for s in sectors},
    }
