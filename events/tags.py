from enum import Enum, auto
from typing import List, Dict, Set

class EventTag(Enum):
    """Теги для категоризации событий"""
    # Внутренняя политика
    IDEOLOGY = auto()      # Идеология, пропаганда, культура
    CADRES = auto()        # Кадры, назначения, чистки
    ECONOMY = auto()       # Экономика, реформы, план
    AGRICULTURE = auto()   # Сельское хозяйство, целина
    SOCIAL = auto()        # Социальная сфера, жильё, здравоохранение
    SCIENCE = auto()       # 🔹 Наука, исследования, технологии (добавлено!)
    
    # Внешняя политика
    FOREIGN = auto()       # Дипломатия, разрядка, саммиты
    DEFENSE = auto()       # Оборона, ВПК, ядерный паритет
    SPACE = auto()         # Космос, пилотируемые программы
    SOCIALIST_BLOC = auto() # Страны соцлагеря, ОВД, СЭВ
    DEVELOPING = auto()    # Развивающиеся страны, помощь
    
    # Кризисы и ЧП
    CRISIS = auto()        # Внутренние кризисы, диссиденты, самиздат
    INTERNATIONAL = auto() # Международные кризисы, конфликты
    DISASTER = auto()      # Природные/техногенные катастрофы

# Словарь для быстрого поиска по строке
TAG_MAP = {tag.name.lower(): tag for tag in EventTag}

def parse_tags(tag_strings: List[str]) -> Set[EventTag]:
    """Преобразует список строк в набор тегов"""
    result = set()
    for t in tag_strings:
        key = t.strip().lower()
        if key in TAG_MAP:
            result.add(TAG_MAP[key])
    return result

def get_tag_name(tag: EventTag) -> str:
    """Человекочитаемое название тега"""
    names = {
        EventTag.IDEOLOGY: "Идеология",
        EventTag.CADRES: "Кадры",
        EventTag.ECONOMY: "Экономика",
        EventTag.AGRICULTURE: "Сельское хозяйство",
        EventTag.SOCIAL: "Социальная сфера",
        EventTag.SCIENCE: "Наука",          # 🔹 Добавлено
        EventTag.FOREIGN: "Внешняя политика",
        EventTag.DEFENSE: "Оборона",
        EventTag.SPACE: "Космос",
        EventTag.SOCIALIST_BLOC: "Соцлагерь",
        EventTag.DEVELOPING: "Развивающиеся страны",
        EventTag.CRISIS: "Кризис",
        EventTag.INTERNATIONAL: "Международный кризис",
        EventTag.DISASTER: "ЧП",
    }
    return names.get(tag, tag.name)