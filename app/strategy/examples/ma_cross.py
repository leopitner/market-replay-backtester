from app.strategy.base import Strategy

class MACrossStrategy(Strategy):
    def __init__(self, fast=5, slow=20, **kw):
        super().__init__(**kw)
        self.fast, self.slow = fast, slow
        self.prices = []

    def on_bar(self, bar) -> int:
        self.prices.append(bar["close"])
        if len(self.prices) < self.slow:
            return 0
        fast_ma = sum(self.prices[-self.fast:]) / self.fast
        slow_ma = sum(self.prices[-self.slow:]) / self.slow
        return 1 if fast_ma > slow_ma else -1