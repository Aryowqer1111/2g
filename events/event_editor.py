import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from events.tags import EventTag

# 🔹 Запрещённые понятия (фантастика, мистика, абсурд)
IMPOSSIBLE_KEYWORDS = {
    "галактика", "инопланетяне", "магия", "колдовство", "бессмертие",
    "машина времени", "телепортация", "воскрешение", "чудо", "летающие тарелки",
    "вечный двигатель", "антигравитация", "заговор рептилоидов", "НЛО"
}

# 🔹 Исторически достоверные термины СССР 1960-1991
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
    """Структура пользовательского события"""
    title: str
    description: str
    tags: List[EventTag]
    choices: List[Dict]
    year: int
    author: str = "Игрок"
    plausibility_score: float = 0.5

def check_plausibility(text: str, year: int) -> Tuple[float, List[str]]:
    """
    Проверяет реалистичность события.
    Возвращает: (оценка 0.0–1.0, список предупреждений)
    """
    warnings = []
    text_lower = text.lower()

    # Минимальная длина
    if len(text) < 15:
        return 0.0, ["Текст слишком короткий. Опишите ситуацию подробнее."]

    # 1. Блокировка фантастики/абсурда
    found_impossible = [kw for kw in IMPOSSIBLE_KEYWORDS if kw in text_lower]
    if found_impossible:
        return 0.1, [f"Нереалистичные понятия: {', '.join(found_impossible)}"]

    # 2. Базовая оценка за структуру
    score = 0.4
    if len(text) > 40: score += 0.1
    if re.search(r'\d{3,}', text): score += 0.1  # Наличие цифр/фактов повышает достоверность

    # 3. Бонус за исторические термины
    found_valid = [kw for kw in VALID_TOPICS if kw in text_lower]
    score += min(0.3, len(found_valid) * 0.1)

    # 4. Проверка года
    if year < 1960 or year > 1991:
        warnings.append(f"Год {year} выходит за рамки симуляции (1960–1991)")
        score -= 0.2

    final_score = max(0.0, min(1.0, score))
    return final_score, warnings