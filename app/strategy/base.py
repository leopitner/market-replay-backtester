class Strategy:
    def __init__(self, **params):
        self.params = params

    def on_bar(self, bar) -> int | None:
        """
        Return target position (-1, 0, 1) or None to hold current position.
        """
        return None