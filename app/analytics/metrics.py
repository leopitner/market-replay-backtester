import numpy as np
from app.engine.backtest_engine import Result

def summarize(result: Result, periods_per_year: int = 252) -> dict:
    eq = result.equity_curve
    if len(eq) < 2:
        return {"trades": len(result.ledger), "final_equity": 0.0, "sharpe": 0.0}
        
    ret = eq.pct_change().dropna()
    
    sharpe = 0.0
    if ret.std() > 0:
        sharpe = float((ret.mean() / ret.std()) * np.sqrt(periods_per_year))
        
    return {
        "trades": len(result.ledger),
        "final_equity": float(eq.iloc[-1]),
        "sharpe": round(sharpe, 3),
        "max_drawdown": float((eq / eq.cummax() - 1).min())
    }