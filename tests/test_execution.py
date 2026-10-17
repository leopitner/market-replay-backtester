import pandas as pd
from pathlib import Path
from app.engine.backtest_engine import BacktestEngine
from app.strategy.base import Strategy

class BuyAndHold(Strategy):
    def on_bar(self, bar):
        if bar.name == 0:
            return 1
        return None

def test_next_bar_execution_and_ledger():
    bars = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=3, freq="D"),
        "open": [100.0, 110.0, 120.0],
        "high": [100.0, 110.0, 120.0],
        "low": [100.0, 110.0, 120.0],
        "close": [100.0, 110.0, 120.0],
        "volume": [100, 100, 100]
    })
    
    engine = BacktestEngine(initial_cash=10000, slippage_bps=0)
    result = engine.run(bars, BuyAndHold())
    
    assert len(result.ledger) == 1
    fill = result.ledger.iloc[0]
    
    assert fill["execution_time"] == bars["timestamp"].iloc[1]
    assert fill["price"] == 110.0
    assert fill["quantity"] == 1
    assert fill["position"] == 1
    
    assert fill["cash"] == 9890.0
    
    
    assert result.equity_curve.iloc[0] == 10000.0
    assert result.equity_curve.iloc[1] == 10000.0
    assert result.equity_curve.iloc[2] == 10010.0