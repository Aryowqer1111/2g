import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Advisor:
    name: str
    faction: str
    competence: float = 50.0
    loyalty: float = 60.0
    is_betraying: bool = False
    tenure_months: int = 0

@dataclass
class FactionMember:
    name: str
    internal_influence: float = 50.0
    age: int = 55
    birth_year: int = 1905
    health: float = 80.0
    is_current_leader: bool = False
    is_politburo_member: bool = False
    
    def check_mortality(self) -> bool:
        if self.age < 65: base_chance = 0.001
        elif self.age < 75: base_chance = 0.01
        else: base_chance = 0.03 + (self.age - 75) * 0.005
        health_factor = 1.0 + (100.0 - self.health) / 100.0
        return random.random() < (base_chance * health_factor)
    
    def age_up(self):
        self.age += 1/12
        if self.age > 60:
            self.health = max(10.0, self.health - random.uniform(0.1, 0.4))

@dataclass
class PolitburoCandidate:
    name: str
    faction: str
    age: int
    experience: float
    support_base: float

@dataclass
class Faction:
    name: str
    leader: str
    influence: float = 50.0
    loyalty: float = 50.0
    ideology: str = ""
    agenda: List[str] = field(default_factory=list)
    rivals: List[str] = field(default_factory=list)
    members: List[FactionMember] = field(default_factory=list)
    advisor: Optional[Advisor] = None
    # 🔹 НОВЫЕ ПОЛЯ: Приоритеты фракции (0.0–1.0) и толерантность к риску
    priorities: Dict[str, float] = field(default_factory=dict)
    risk_tolerance: float = 0.5

def get_1960_start() -> Dict[str, Faction]:
    from factions.names import generate_ussr_name
    factions = {
        "Идеологи": Faction(
            "Идеологи", "М. Суслов", 60.0, 55.0, "Ортодоксальный марксизм", 
            ["Чистка культуры", "Идеологический контроль"], ["Реформаторы"],
            priorities={"stability": 0.9, "ideology": 0.95, "economy": 0.4, "defense": 0.6, "social": 0.3},
            risk_tolerance=0.2
        ),
        "Реформаторы": Faction(
            "Реформаторы", "А. Косыгин", 45.0, 65.0, "Технократия и хозрасчёт", 
            ["Экономические реформы", "Децентрализация"], ["Идеологи", "КГБ"],
            priorities={"stability": 0.5, "ideology": 0.3, "economy": 0.95, "defense": 0.4, "social": 0.7, "innovation": 0.8},
            risk_tolerance=0.8
        ),
        "ВПК": Faction(
            "ВПК", "Д. Устинов", 70.0, 50.0, "Военно-промышленный приоритет", 
            ["Ядерный паритет", "Космос", "Модернизация армии"], ["Реформаторы"],
            priorities={"stability": 0.7, "ideology": 0.5, "economy": 0.6, "defense": 0.98, "social": 0.4},
            risk_tolerance=0.3
        ),
        "КГБ": Faction(
            "КГБ", "Ю. Андропов", 55.0, 60.0, "Госбезопасность и контроль", 
            ["Борьба с коррупцией", "Подавление инакомыслия"], ["Реформаторы", "Интеллигенция"],
            priorities={"stability": 0.95, "ideology": 0.8, "economy": 0.5, "defense": 0.7, "social": 0.2},
            risk_tolerance=0.1
        ),
        "Регионы": Faction(
            "Регионы", "Л. Брежнев", 50.0, 70.0, "Клановость и местные элиты", 
            ["Кадровая политика", "Бюджетные дотации"], ["КГБ", "Идеологи"],
            priorities={"stability": 0.6, "ideology": 0.4, "economy": 0.8, "defense": 0.5, "social": 0.7},
            risk_tolerance=0.6
        )
    }

    for fac in factions.values():
        fac.members.append(FactionMember(name=fac.leader, internal_influence=80.0, age=58, birth_year=1960-58, is_current_leader=True))
        for _ in range(random.randint(3, 4)):
            fac.members.append(FactionMember(
                name=generate_ussr_name(), internal_influence=random.uniform(20, 65), 
                age=random.randint(45, 70), birth_year=1960 - random.randint(45, 70)
            ))
        fac.advisor = Advisor(name=fac.leader.split()[0] + " " + fac.leader.split()[1][0]+".", faction=fac.name, loyalty=fac.loyalty)
    return factions