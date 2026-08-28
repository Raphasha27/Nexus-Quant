import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from pydantic import ValidationError
from api.main import SignalRequest, PortfolioRequest, AnomalyRequest, generate_ohlcv


class TestSignalRequest:
    def test_defaults(self):
        req = SignalRequest()
        assert req.ticker == "NQ-SYNTH"
        assert req.strategy == "momentum"
        assert req.risk_tolerance == 0.5

    def test_custom_values(self):
        req = SignalRequest(ticker="AAPL", strategy="mean_reversion", risk_tolerance=0.8)
        assert req.ticker == "AAPL"
        assert req.strategy == "mean_reversion"
        assert req.risk_tolerance == 0.8

    def test_optional_fields_default_when_omitted(self):
        req = SignalRequest(ticker="TSLA")
        assert req.ticker == "TSLA"
        assert req.strategy == "momentum"
        assert req.risk_tolerance == 0.5

    def test_invalid_field_type_rejected(self):
        with pytest.raises(ValidationError):
            SignalRequest(ticker=123)

    def test_extra_fields_ignored(self):
        req = SignalRequest(ticker="X", extra="ignored")
        assert req.ticker == "X"


class TestPortfolioRequest:
    def test_defaults(self):
        req = PortfolioRequest()
        assert req.tickers == ["NQ-A", "NQ-B", "NQ-C"]
        assert req.capital == 100000.0

    def test_custom_tickers(self):
        req = PortfolioRequest(tickers=["AAPL", "MSFT"], capital=50000.0)
        assert req.tickers == ["AAPL", "MSFT"]
        assert req.capital == 50000.0

    def test_empty_tickers_list(self):
        req = PortfolioRequest(tickers=[], capital=10000.0)
        assert req.tickers == []

    def test_invalid_capital_type(self):
        with pytest.raises(ValidationError):
            PortfolioRequest(capital="not_a_number")

    def test_invalid_tickers_type(self):
        with pytest.raises(ValidationError):
            PortfolioRequest(tickers="not_a_list")


class TestAnomalyRequest:
    def test_defaults(self):
        req = AnomalyRequest()
        assert req.ticker == "NQ-SYNTH"
        assert req.lookback_days == 30

    def test_custom_values(self):
        req = AnomalyRequest(ticker="SPY", lookback_days=60)
        assert req.ticker == "SPY"
        assert req.lookback_days == 60

    def test_invalid_lookback_type(self):
        with pytest.raises(ValidationError):
            AnomalyRequest(lookback_days="thirty")


class TestGenerateOHLV:
    def test_returns_list(self):
        data = generate_ohlcv()
        assert isinstance(data, list)

    def test_default_length(self):
        data = generate_ohlcv()
        assert len(data) == 50

    def test_custom_length(self):
        data = generate_ohlcv(n=10)
        assert len(data) == 10

    def test_single_candle(self):
        data = generate_ohlcv(n=1)
        assert len(data) == 1

    def test_candle_structure(self):
        data = generate_ohlcv(n=1)
        candle = data[0]
        expected_keys = {"date", "open", "high", "low", "close", "volume"}
        assert set(candle.keys()) == expected_keys

    def test_candle_types(self):
        data = generate_ohlcv(n=1)
        candle = data[0]
        assert isinstance(candle["date"], str)
        assert isinstance(candle["open"], float)
        assert isinstance(candle["high"], float)
        assert isinstance(candle["low"], float)
        assert isinstance(candle["close"], float)
        assert isinstance(candle["volume"], int)

    def test_high_gte_low(self):
        for _ in range(20):
            data = generate_ohlcv(n=5)
            for candle in data:
                assert candle["high"] >= candle["low"]

    def test_volume_positive(self):
        data = generate_ohlcv(n=50)
        for candle in data:
            assert candle["volume"] > 0

    def test_date_format(self):
        data = generate_ohlcv(n=5)
        for candle in data:
            parts = candle["date"].split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 4
            assert len(parts[1]) == 2
            assert len(parts[2]) == 2

    def test_custom_base_price(self):
        data = generate_ohlcv(base=500.0, n=5)
        for candle in data:
            assert candle["open"] > 0

    def test_zero_length(self):
        data = generate_ohlcv(n=0)
        assert data == []
