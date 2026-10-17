from dataclasses import dataclass, field
import pandas as pd
from app.broker.simulated_broker import SimulatedBroker

@dataclass
class Result:
    equity_curve: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))
    ledger: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    final_cash: float = 0.0

class BacktestEngine:
    def __init__(self, initial_cash=100_000, slippage_bps=5):
        self.broker = SimulatedBroker(initial_cash=initial_cash, slippage_bps=slippage_bps)

    def run(self, bars: pd.DataFrame, strategy) -> Result:
        equity = []
        pending_target = None
        pending_time = None

        for i in range(len(bars)):
            bar = bars.iloc[i]
            
            if pending_target is not None:
                self.broker.execute_target_position(
                    decision_time=pending_time,
                    execution_time=bar["timestamp"],
                    target_qty=pending_target,
                    price=bar["open"]
                )
                pending_target = None

            target = strategy.on_bar(bar)
            if target is not None:
                pending_target = target
                pending_time = bar["timestamp"]

            # 3. Mark-to-market equity
            current_equity = self.broker.cash + (self.broker.position * bar["close"])
            equity.append(current_equity)

        return Result(
            equity_curve=pd.Series(equity, index=bars["timestamp"]),
            ledger=pd.DataFrame(self.broker.ledger),
            final_cash=self.broker.cash,
        )