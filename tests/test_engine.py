from pathlib import Path
from app.data.loader import load_bars
from app.engine.backtest_engine import BacktestEngine
from app.strategy.examples.ma_cross import MACrossStrategy

def test_backtest_runs_and_produces_equity():
    bars = load_bars(Path("data/sample.csv"))
    result = BacktestEngine().run(bars, MACrossStrategy(fast=5, slow=20))
    assert len(result.equity_curve) == len(bars)
    assert result.final_cash > 0

def test_missing_columns_raises(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("timestamp,close\n2024-01-01,1\n")
    import pytest
    with pytest.raises(ValueError):
        load_bars(bad)