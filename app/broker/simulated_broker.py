class SimulatedBroker:
    def __init__(self, initial_cash=100_000, slippage_bps=5, commission=0.0):
        self.cash = initial_cash
        self.position = 0
        self.slippage_bps = slippage_bps
        self.commission = commission

    def fill(self, side: int, qty: int, price: float) -> float:
        fill_price = price * (1 + side * self.slippage_bps / 10_000)
        self.cash -= side * qty * fill_price + self.commission
        self.position += side * qty
        return fill_price