import pandas as pd
from app.engine.backtest_engine import BacktestEngine
from app.strategy.base import Strategy

class BuyAndHold(Strategy):
    def on_bar(self, bar):
        if bar.name == 0:
            return 1
        return None

def test_next_bar_execution_with_slippage():
    bars = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=3, freq="D"),
        "open": [100.0, 110.0, 120.0],
        "high": [100.0, 110.0, 120.0],
        "low": [100.0, 110.0, 120.0],
        "close": [100.0, 110.0, 120.0],
        "volume": [100, 100, 100]
    })
    
    engine = BacktestEngine(initial_cash=10000, slippage_bps=5)
    result = engine.run(bars, BuyAndHold())
    
    assert len(result.ledger) == 1
    fill = result.ledger.iloc[0]
    
    expected_fill_price = 110.055
    
    assert fill["execution_time"] == bars["timestamp"].iloc[1]
    assert round(fill["fill_price"], 3) == expected_fill_price
    assert fill["quantity"] == 1
    assert fill["position"] == 1
    
    assert round(fill["cash"], 3) == 9889.945
    
    assert round(fill["slippage_cost"], 3) == 0.055