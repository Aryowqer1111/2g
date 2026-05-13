import re
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from events.tags import EventTag

IMPOSSIBLE_KEYWORDS = {
    "галактика", "инопланетяне", "магия", "колдовство", "бессмертие",
    "машина времени", "телепортация", "воскрешение", "чудо", "летающие тарелки",
    "вечный двигатель", "антигравитация", "заговор рептилоидов", "НЛО"
}

VALID_TOPICS = {
    "экономика", "реформа", "план", "пятилетка", "хозрасчёт", "прибыль",
    "сельское хозяйство", "целина", "урожай", "зерно", "мясо", "молоко",
    "космос", "спутник", "ракета", "орбита", "станция",
    "оборона", "армия", "флот", "авиация", "ядерный", "паритет",
    "дипломатия", "саммит", "договор", "разрядка", "ОСВ", "СБСЕ",
    "идеология", "партия", "съезд", "пленум", "постановление",
    "культура", "кино", "театр", "литература",
    "наука", "академия", "институт", "открытие", "патент",
    "социальная", "жильё", "квартира", "больница", "школа",
    "внешняя политика", "помощь", "сотрудничество", "экспорт", "импорт",
}

@dataclass
class CustomEvent:
    # 🔹 Обязательные поля идут ПЕРВЫМИ
    title: str
    description: str
    tags: List[EventTag]
    choices: List[Dict]
    year: int
    # 🔹 Поля со значениями по умолчанию идут ПОСЛЕДНИМИ
    author: str = "Игрок"
    plausibility_score: float = 0.5
    id: str = field(default_factory=lambda: f"cust_{random.randint(10000, 99999)}")

def check_plausibility(text: str, year: int) -> Tuple[float, List[str]]:
    warnings = []
    text_lower = text.lower()
    if len(text) < 15:
        return 0.0, ["Текст слишком короткий. Опишите ситуацию подробнее."]
    found_impossible = [kw for kw in IMPOSSIBLE_KEYWORDS if kw in text_lower]
    if found_impossible:
        return 0.1, [f"Нереалистичные понятия: {', '.join(found_impossible)}"]
    score = 0.4
    if len(text) > 40: score += 0.1
    if re.search(r'\d{3,}', text): score += 0.1
    found_valid = [kw for kw in VALID_TOPICS if kw in text_lower]
    score += min(0.3, len(found_valid) * 0.1)
    if year < 1960 or year > 1991:
        warnings.append(f"Год {year} выходит за рамки симуляции (1960–1991)")
        score -= 0.2
    return max(0.0, min(1.0, score)), warnings