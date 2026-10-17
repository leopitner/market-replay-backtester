import heapq
from .event import Event

class EventLoop:
    def __init__(self):
        self._queue = []

    def push(self, event: Event):
        heapq.heappush(self._queue, event)

    def run(self, handlers: dict):
        while self._queue:
            event = heapq.heappop(self._queue)
            handler = handlers.get(type(event).__name__)
            if handler:
                handler(event)