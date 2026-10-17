from dataclasses import dataclass, field
import pandas as pd
from app.broker.simulated_broker import SimulatedBroker

@dataclass
class Result:
    equity_curve: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))
    trades: int = 0
    final_cash: float = 0.0

class BacktestEngine:
    def __init__(self, initial_cash=100_000):
        self.broker = SimulatedBroker(initial_cash=initial_cash)

    def run(self, bars: pd.DataFrame, strategy) -> Result:
        equity = []
        trades = 0
        for _, bar in bars.iterrows():
            signal = strategy.on_bar(bar)          # -1, 0, +1
            if signal:
                self.broker.fill(signal, 1, bar["close"])
                trades += 1
            equity.append(self.broker.cash + self.broker.position * bar["close"])
        return Result(
            equity_curve=pd.Series(equity, index=bars["timestamp"]),
            trades=trades,
            final_cash=self.broker.cash,
        )