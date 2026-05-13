from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class GameState:
    year: int = 1960
    month: int = 1
    turn_counter: int = 0
    stability: float = 65.0
    budget: float = 50.0
    support: float = 60.0
    ideology: float = 70.0
    gdp_index: float = 100.0  # Индекс ВВП (1960 = 100)
    extensions: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)

    @staticmethod
    def clamp(val: float) -> float:
        return max(0.0, min(100.0, val))

    def update_metric(self, key: str, delta: float):
        if hasattr(self, key) and isinstance(getattr(self, key), (int, float)):
            setattr(self, key, self.clamp(getattr(self, key) + delta))

    def set_ext(self, section: str, key: str, value: Any):
        self.extensions.setdefault(section, {})[key] = value

    def get_ext(self, section: str, key: str, default=None):
        return self.extensions.get(section, {}).get(key, default)

    def log_event(self, msg: str):
        self.history.append({"turn": self.turn_counter, "date": f"{self.month}.{self.year}", "msg": msg})
