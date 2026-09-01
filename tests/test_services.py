import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import generate_ohlcv

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestSignalGeneration:
    def test_signal_endpoint_returns_valid_structure(self):
        resp = client.post("/api/v1/signal", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert "ticker" in data
        assert "strategy" in data
        assert "signal" in data
        assert "confidence" in data
        assert "indicators" in data
        assert "generated_at" in data

    def test_signal_is_one_of_valid_values(self):
        resp = client.post("/api/v1/signal", json={})
        assert resp.json()["signal"] in ("BUY", "SELL", "HOLD")

    def test_signal_confidence_range(self):
        for _ in range(30):
            resp = client.post("/api/v1/signal", json={})
            confidence = resp.json()["confidence"]
            assert 0.6 <= confidence <= 0.95

    def test_signal_indicators_present(self):
        resp = client.post("/api/v1/signal", json={})
        indicators = resp.json()["indicators"]
        assert "sma_5" in indicators
        assert "sma_20" in indicators
        assert "rsi" in indicators

    def test_signal_rsi_range(self):
        for _ in range(30):
            resp = client.post("/api/v1/signal", json={})
            rsi = resp.json()["indicators"]["rsi"]
            assert 20 <= rsi <= 80

    def test_signal_with_custom_ticker(self):
        resp = client.post("/api/v1/signal", json={"ticker": "GOOG"})
        assert resp.json()["ticker"] == "GOOG"

    def test_signal_with_custom_strategy(self):
        resp = client.post("/api/v1/signal", json={"strategy": "mean_reversion"})
        assert resp.json()["strategy"] == "mean_reversion"

    def test_signal_timestamp_format(self):
        resp = client.post("/api/v1/signal", json={})
        ts = resp.json()["generated_at"]
        assert "T" in ts


class TestAnomalyDetection:
    def test_anomaly_endpoint_structure(self):
        resp = client.post("/api/v1/anomaly", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert "ticker" in data
        assert "lookback_days" in data
        assert "anomalies_detected" in data
        assert "anomalies" in data
        assert "avg_volume" in data
        assert "alert" in data

    def test_anomaly_returns_list(self):
        resp = client.post("/api/v1/anomaly", json={})
        assert isinstance(resp.json()["anomalies"], list)

    def test_anomaly_count_matches_list(self):
        resp = client.post("/api/v1/anomaly", json={})
        data = resp.json()
        assert data["anomalies_detected"] == len(data["anomalies"])

    def test_anomaly_list_item_structure(self):
        resp = client.post("/api/v1/anomaly", json={"lookback_days": 50})
        anomalies = resp.json()["anomalies"]
        if anomalies:
            item = anomalies[0]
            assert "date" in item
            assert "volume" in item
            assert "z_score" in item

    def test_anomaly_z_score_significant(self):
        resp = client.post("/api/v1/anomaly", json={"lookback_days": 50})
        for a in resp.json()["anomalies"]:
            assert abs(a["z_score"]) > 1.0

    def test_anomaly_alert_boolean(self):
        resp = client.post("/api/v1/anomaly", json={})
        assert isinstance(resp.json()["alert"], bool)

    def test_anomaly_lookback_days_reflected(self):
        resp = client.post("/api/v1/anomaly", json={"lookback_days": 15})
        assert resp.json()["lookback_days"] == 15

    def test_anomaly_avg_volume_positive(self):
        resp = client.post("/api/v1/anomaly", json={})
        assert resp.json()["avg_volume"] > 0

    def test_anomaly_with_different_tickers(self):
        for ticker in ["AAPL", "MSFT", "TSLA"]:
            resp = client.post("/api/v1/anomaly", json={"ticker": ticker})
            assert resp.json()["ticker"] == ticker


class TestBacktesting:
    def _run_backtest(self, strategy, signals_needed=20):
        signals = []
        for _ in range(signals_needed):
            resp = client.post("/api/v1/signal", json={"strategy": strategy})
            signals.append(resp.json()["signal"])
        return signals

    def test_momentum_strategy_produces_signals(self):
        signals = self._run_backtest("momentum")
        assert len(signals) == 20
        assert all(s in ("BUY", "SELL", "HOLD") for s in signals)

    def test_mean_reversion_strategy_produces_signals(self):
        signals = self._run_backtest("mean_reversion")
        assert len(signals) == 20
        assert all(s in ("BUY", "SELL", "HOLD") for s in signals)

    def test_signals_not_all_same(self):
        signals = self._run_backtest("random", signals_needed=50)
        assert len(set(signals)) > 1

    def test_signal_distribution(self):
        signals = self._run_backtest("mixed", signals_needed=200)
        counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
        for s in signals:
            counts[s] += 1
        assert counts["BUY"] > 0
        assert counts["SELL"] > 0
        assert counts["HOLD"] > 0


class TestPortfolioOptimization:
    def _optimize(self, tickers, capital=100000.0):
        resp = client.post(
            "/api/v1/portfolio/optimize", json={"tickers": tickers, "capital": capital}
        )
        return resp.json()

    def test_optimization_returns_allocations(self):
        data = self._optimize(["A", "B", "C"])
        assert "allocations" in data

    def test_allocation_keys_match_tickers(self):
        tickers = ["AAPL", "MSFT", "GOOG"]
        data = self._optimize(tickers)
        assert set(data["allocations"].keys()) == set(tickers)

    def test_weights_sum_to_one(self):
        data = self._optimize(["X", "Y", "Z", "W"])
        total_weight = sum(a["weight"] for a in data["allocations"].values())
        assert abs(total_weight - 1.0) < 0.01

    def test_capital_allocation_matches_total(self):
        capital = 250000.0
        data = self._optimize(["A", "B"], capital=capital)
        total_allocated = sum(a["capital_usd"] for a in data["allocations"].values())
        assert abs(total_allocated - capital) < 1.0

    def test_expected_return_range(self):
        for _ in range(10):
            data = self._optimize(["A", "B"])
            assert 0.08 <= data["expected_return"] <= 0.22

    def test_sharpe_ratio_range(self):
        for _ in range(10):
            data = self._optimize(["A", "B"])
            assert 1.2 <= data["sharpe_ratio"] <= 2.8

    def test_max_drawdown_range(self):
        for _ in range(10):
            data = self._optimize(["A", "B"])
            assert 0.05 <= data["max_drawdown"] <= 0.18

    def test_single_ticker_portfolio(self):
        data = self._optimize(["ONLY"])
        assert len(data["allocations"]) == 1
        weight = list(data["allocations"].values())[0]["weight"]
        assert abs(weight - 1.0) < 0.01

    def test_many_tickers(self):
        tickers = [f"TICK{i}" for i in range(20)]
        data = self._optimize(tickers)
        assert len(data["allocations"]) == 20


class TestOHLCVDataQuality:
    def test_ohlcv_ohlc_consistency(self):
        data = generate_ohlcv(base=100.0, n=50)
        for candle in data:
            assert candle["high"] >= candle["open"]
            assert candle["high"] >= candle["close"]
            assert candle["low"] <= candle["open"]
            assert candle["low"] <= candle["close"]

    def test_ohlcv_reasonable_price_range(self):
        data = generate_ohlcv(base=200.0, n=50)
        for candle in data:
            assert 0 < candle["high"] < 1000
            assert 0 < candle["low"] < 1000
            assert 0 < candle["open"] < 1000
            assert 0 < candle["close"] < 1000

    def test_ohlcv_volume_realistic(self):
        data = generate_ohlcv(n=100)
        for candle in data:
            assert 100_000 <= candle["volume"] <= 5_000_000


class TestMarketSummary:
    def test_summary_structure(self):
        resp = client.get("/api/v1/market/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert "timestamp" in data
        assert "market_sentiment" in data
        assert "vix" in data
        assert "sector_performance" in data

    def test_sentiment_valid_value(self):
        resp = client.get("/api/v1/market/summary")
        assert resp.json()["market_sentiment"] in ("Bullish", "Bearish", "Neutral")

    def test_vix_range(self):
        resp = client.get("/api/v1/market/summary")
        vix = resp.json()["vix"]
        assert 12 <= vix <= 35

    def test_sector_performance_keys(self):
        resp = client.get("/api/v1/market/summary")
        sectors = set(resp.json()["sector_performance"].keys())
        expected = {"Technology", "Finance", "Healthcare", "Energy", "Consumer"}
        assert sectors == expected

    def test_sector_performance_values(self):
        resp = client.get("/api/v1/market/summary")
        for sector, perf in resp.json()["sector_performance"].items():
            assert -3 <= perf <= 5


class TestOHLCVEndpoint:
    def test_ohlcv_returns_correct_days(self):
        for days in [5, 10, 30, 60]:
            resp = client.get(f"/api/v1/ohlcv/TEST?days={days}")
            assert len(resp.json()["data"]) == days

    def test_ohlcv_default_days(self):
        resp = client.get("/api/v1/ohlcv/TEST")
        assert len(resp.json()["data"]) == 30

    def test_ohlcv_ticker_reflected(self):
        resp = client.get("/api/v1/ohlcv/SPY")
        assert resp.json()["ticker"] == "SPY"
