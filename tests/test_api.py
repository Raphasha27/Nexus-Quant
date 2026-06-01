import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ONLINE"
    assert data["platform"] == "Nexus-Quant"
    assert "modes" in data


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_generate_signal():
    resp = client.post("/api/v1/signal", json={"ticker": "TEST", "strategy": "momentum"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "TEST"
    assert data["signal"] in ("BUY", "SELL", "HOLD")
    assert "indicators" in data


def test_detect_anomaly():
    resp = client.post("/api/v1/anomaly", json={"ticker": "TEST", "lookback_days": 30})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "TEST"
    assert "anomalies" in data


def test_get_ohlcv():
    resp = client.get("/api/v1/ohlcv/TEST?days=10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "TEST"
    assert len(data["data"]) == 10


def test_portfolio_optimize():
    resp = client.post("/api/v1/portfolio/optimize", json={
        "tickers": ["A", "B", "C"],
        "capital": 100000.0
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["strategy"] == "mean_variance_optimization"
    assert "allocations" in data


def test_market_summary():
    resp = client.get("/api/v1/market/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "market_sentiment" in data
    assert "sector_performance" in data
