class SimulatedBroker:
    def __init__(self, initial_cash=100_000, slippage_bps=5, commission=0.0):
        self.cash = initial_cash
        self.position = 0
        self.slippage_bps = slippage_bps
        self.commission = commission
        self.ledger = []

    def execute_target_position(self, decision_time, execution_time, target_qty: int, price: float):
        delta = target_qty - self.position
        if delta == 0:
            return

        side = 1 if delta > 0 else -1
        
        fill_price = price * (1 + side * self.slippage_bps / 10_000)
        
        fees = abs(delta) * self.commission
        
        slippage_cost = abs(delta) * abs(fill_price - price)
        
        self.cash -= (delta * fill_price) + fees
        self.position = target_qty

        self.ledger.append({
            "decision_time": decision_time,
            "execution_time": execution_time,
            "side": "BUY" if side == 1 else "SELL",
            "quantity": abs(delta),
            "reference_price": price,
            "fill_price": fill_price,
            "slippage_cost": slippage_cost,
            "fees": fees,
            "cash": self.cash,
            "position": self.position
        })