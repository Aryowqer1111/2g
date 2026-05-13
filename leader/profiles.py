from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class LeaderProfile:
    name: str
    period: Tuple[int, int]
    authority: float  # 50-100
    preferred_strategy: str  # "military", "economy", "social", "ideology"
    risk_tolerance: float  # 0.0-1.0
    faction_bias: Dict[str, float]  # faction_name: loyalty_shift
    historical_traits: List[str]

HISTORICAL_LEADERS = {
    "khrushchev": LeaderProfile("Н.С. Хрущёв", (1953, 1964), 65.0, "social", 0.85,
                                {"Идеологи": -10, "Реформаторы": 15, "Регионы": 10, "ВПК": -5},
                                ["Импульсивный", "Антисталинист", "Целинник", "Реформатор"]),
    "brezhnev": LeaderProfile("Л.И. Брежнев", (1964, 1982), 80.0, "ideology", 0.25,
                              {"Идеологи": 10, "ВПК": 15, "Регионы": 20, "КГБ": 5},
                              ["Стабильность", "Коллективное руководство", "Кадровый консерватизм"]),
    "andropov": LeaderProfile("Ю.В. Андропов", (1982, 1984), 75.0, "ideology", 0.6,
                              {"КГБ": 25, "Идеологи": 10, "Реформаторы": -5, "ВПК": 0},
                              ["Дисциплина", "Антикоррупция", "Технократ", "Жёсткий контроль"]),
    "chernenko": LeaderProfile("К.У. Черненко", (1984, 1985), 50.0, "ideology", 0.1,
                               {"Идеологи": 15, "Реформаторы": -10, "Регионы": 5, "КГБ": 0},
                               ["Статус-кво", "Консерватор", "Здоровье слабое"])
}