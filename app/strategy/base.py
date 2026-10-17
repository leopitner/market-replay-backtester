class Strategy:
    def __init__(self, **params):
        self.params = params

    def on_bar(self, bar) -> int:
        return 0