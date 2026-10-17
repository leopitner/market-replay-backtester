from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class Event:
    timestamp: float
    priority: int = field(default=0, compare=False)
    data: Any = field(compare=False)