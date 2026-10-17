import json
from . import __name__ as _  # noqa
from app.engine.backtest_engine import Result

def summarize(result: Result) -> dict:
    eq = result.equity_curve
    ret = eq.pct_change().dropna()
    sharpe = float(ret.mean() / ret.std() * (252 ** 0.5)) if len(ret) > 1 and ret.std() else 0.0
    return {
        "trades": result.trades,
        "final_equity": float(eq.iloc[-1]) if len(eq) else 0.0,
        "sharpe": round(sharpe, 3),
    }