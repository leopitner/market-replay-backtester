import numpy as np
from app.engine.backtest_engine import Result

def summarize(result: Result, periods_per_year: int = 252) -> dict:
    eq = result.equity_curve
    trades = len(result.ledger) if not result.ledger.empty else 0
    
    if len(eq) == 0:
        return {"trades": 0, "final_equity": 0.0, "sharpe": 0.0, "max_drawdown": 0.0}
        
    final_equity = float(eq.iloc[-1])
    
    if len(eq) < 2:
        return {"trades": trades, "final_equity": final_equity, "sharpe": 0.0, "max_drawdown": 0.0}
        
    ret = eq.pct_change().dropna()
    
    sharpe = 0.0
    if ret.std() > 0:
        sharpe = float((ret.mean() / ret.std()) * np.sqrt(periods_per_year))
        
    max_dd = float((eq / eq.cummax() - 1).min())
    
    return {
        "trades": trades,
        "final_equity": final_equity,
        "sharpe": round(sharpe, 3),
        "max_drawdown": round(max_dd, 3)
    }