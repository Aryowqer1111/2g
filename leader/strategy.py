from typing import Dict
from core.state import GameState
from economy.engine import EconomyEngine
from factions.ai_engine import FactionAI

# Используем точные имена атрибутов из EconomyState и точные названия фракций
STRATEGY_VECTORS = {
    "military": {"name": "Военный паритет", "econ": {"vpk": 1.5, "consumer_goods": -0.8}, "faction": {"ВПК": 4, "Реформаторы": -3, "Регионы": -2}},
    "economy": {"name": "Экономический рост", "econ": {"heavy_industry": 1.2, "agriculture": 0.8, "energy": 0.5}, "faction": {"Реформаторы": 4, "Идеологи": -2}},
    "social": {"name": "Социальная политика", "econ": {"consumer_goods": 1.8, "agriculture": 0.5}, "faction": {"Регионы": 5, "ВПК": -2, "Идеологи": -3}},
    "ideology": {"name": "Идеологический контроль", "econ": {"heavy_industry": -0.5, "consumer_goods": -1.0}, "faction": {"Идеологи": 5, "КГБ": 4, "Реформаторы": -6}}
}

class StateStrategy:
    def __init__(self, leader_profile):
        self.vector = leader_profile.preferred_strategy
        self.vectors = STRATEGY_VECTORS

    def apply_monthly(self, state: GameState, economy: EconomyEngine, factions: FactionAI) -> Dict:
        cfg = self.vectors[self.vector]
        log = []

        # Экономика
        for sec, delta in cfg["econ"].items():
            target = getattr(economy.state, sec, None)
            if target and hasattr(target, "efficiency"):
                target.efficiency += delta * 0.1
                target.efficiency = max(10.0, min(95.0, target.efficiency))

        # Фракции
        for fac, delta in cfg["faction"].items():
            if fac in factions.factions:
                factions.factions[fac].loyalty += delta * 0.2
                factions.factions[fac].loyalty = max(5.0, min(100.0, factions.factions[fac].loyalty))

        return {"vector": self.vector, "log": log}

    def switch_vector(self, new_vector: str) -> bool:
        if new_vector in self.vectors:
            self.vector = new_vector
            return True
        return False