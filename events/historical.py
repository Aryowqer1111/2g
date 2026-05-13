from dataclasses import dataclass, field
from typing import List, Dict, Optional
from events.tags import EventTag

@dataclass
class HistoricalEvent:
    """Шаблон исторического события"""
    id: str
    title: str
    description: str
    year_range: tuple  # (min_year, max_year)
    tags: List[EventTag]
    # Эффекты при принятии / отклонении / компромиссе
    effects_accept: Dict[str, float]
    effects_reject: Dict[str, float]
    effects_compromise: Dict[str, float]
    # Требования для доступности
    min_stability: float = 0.0
    required_strategy: Optional[str] = None
    # Историческая достоверность (0-1)
    authenticity: float = 1.0

# 🔹 БАЗА ИСТОРИЧЕСКИХ СОБЫТИЙ 1960-1980 [[1]][[6]][[19]][[27]]
HISTORICAL_EVENTS: Dict[str, HistoricalEvent] = {
    # === ЭКОНОМИКА И РЕФОРМЫ ===
    "kosygin_reform_1965": HistoricalEvent(
        id="kosygin_reform_1965",
        title="Экономическая реформа 1965 года",
        description="Внедрение хозрасчёта, расширение самостоятельности предприятий, переход от валовых показателей к прибыли [[19]].",
        year_range=(1965, 1970),
        tags=[EventTag.ECONOMY, EventTag.CADRES],
        effects_accept={"stability": 4, "budget": 3, "support": 2, "ideology": -2},
        effects_reject={"stability": -3, "budget": -4, "support": -2, "ideology": 3},
        effects_compromise={"stability": 1, "budget": 0, "support": 1, "ideology": 0},
        required_strategy="reform"
    ),
    
    "oil_boom_1973": HistoricalEvent(
        id="oil_boom_1973",
        title="Рост цен на нефть (нефтяной кризис)",
        description="Мировой скачок цен на энергоносители создаёт возможности для экспорта, но усиливает сырьевую зависимость [[1]].",
        year_range=(1973, 1980),
        tags=[EventTag.ECONOMY, EventTag.FOREIGN],
        effects_accept={"stability": 5, "budget": 8, "support": 3, "ideology": -1},
        effects_reject={"stability": -2, "budget": -6, "support": -3, "ideology": 2},
        effects_compromise={"stability": 2, "budget": 3, "support": 1, "ideology": 0},
    ),
    
    "housing_program": HistoricalEvent(
        id="housing_program",
        title="Массовое жилищное строительство",
        description="Расширение программы «хрущёвок» и панельного домостроения для решения жилищного вопроса [[2]].",
        year_range=(1960, 1975),
        tags=[EventTag.SOCIAL, EventTag.ECONOMY],
        effects_accept={"stability": 3, "budget": -4, "support": 6, "ideology": 1},
        effects_reject={"stability": -4, "budget": 2, "support": -5, "ideology": 0},
        effects_compromise={"stability": 0, "budget": -1, "support": 2, "ideology": 0},
    ),
    
    # === ВНЕШНЯЯ ПОЛИТИКА ===
    "detente_1972": HistoricalEvent(
        id="detente_1972",
        title="Разрядка международной напряжённости",
        description="Подписание договоров ОСВ-1 и ПРО с США, визит Никсона в Москву, курс на мирное сосуществование [[13]][[33]].",
        year_range=(1970, 1979),
        tags=[EventTag.FOREIGN, EventTag.DEFENSE],
        effects_accept={"stability": 4, "budget": 2, "support": 3, "ideology": -3},
        effects_reject={"stability": -5, "budget": -3, "support": -4, "ideology": 4},
        effects_compromise={"stability": 1, "budget": 0, "support": 1, "ideology": -1},
        min_stability=40.0
    ),
    
    "helsinki_accords_1975": HistoricalEvent(
        id="helsinki_accords_1975",
        title="Хельсинкские соглашения",
        description="Подписание Заключительного акта СБСЕ: признание послевоенных границ + обязательства по правам человека [[1]].",
        year_range=(1975, 1976),
        tags=[EventTag.FOREIGN, EventTag.IDEOLOGY],
        effects_accept={"stability": 3, "budget": 1, "support": 2, "ideology": -4},
        effects_reject={"stability": -4, "budget": -2, "support": -3, "ideology": 5},
        effects_compromise={"stability": 0, "budget": 0, "support": 0, "ideology": -1},
    ),
    
    "afghanistan_1979": HistoricalEvent(
        id="afghanistan_1979",
        title="Ввод войск в Афганистан",
        description="Решение об оказании интернациональной помощи правительству ДРА для стабилизации обстановки [[1]][[10]].",
        year_range=(1979, 1980),
        tags=[EventTag.FOREIGN, EventTag.DEFENSE, EventTag.CRISIS],
        effects_accept={"stability": -6, "budget": -5, "support": -4, "ideology": 3},
        effects_reject={"stability": 2, "budget": 3, "support": 2, "ideology": -5},
        effects_compromise={"stability": -2, "budget": -1, "support": -1, "ideology": 0},
        min_stability=50.0
    ),
    
    # === НАУКА И КОСМОС ===
    "gagarin_legacy": HistoricalEvent(
        id="gagarin_legacy",
        title="Развитие космической программы",
        description="Запуск новых спутников, орбитальных станций, международное сотрудничество в космосе [[2]][[8]].",
        year_range=(1961, 1980),
        tags=[EventTag.SPACE, EventTag.SCIENCE],
        effects_accept={"stability": 3, "budget": -3, "support": 4, "ideology": 2},
        effects_reject={"stability": -2, "budget": 2, "support": -4, "ideology": -1},
        effects_compromise={"stability": 1, "budget": -1, "support": 1, "ideology": 0},
    ),
    
    # === ИДЕОЛОГИЯ И КУЛЬТУРА ===
    "xxii_congress_1961": HistoricalEvent(
        id="xxii_congress_1961",
        title="XXII съезд КПСС: Программа построения коммунизма",
        description="Принятие Третьей Программы партии и Морального кодекса строителя коммунизма [[7]].",
        year_range=(1961, 1962),
        tags=[EventTag.IDEOLOGY, EventTag.CADRES],
        effects_accept={"stability": 2, "budget": -1, "support": 3, "ideology": 5},
        effects_reject={"stability": -4, "budget": 1, "support": -5, "ideology": -4},
        effects_compromise={"stability": 0, "budget": 0, "support": 0, "ideology": 1},
    ),
    
    "dissident_movement": HistoricalEvent(
        id="dissident_movement",
        title="Рост диссидентского движения",
        description="Появление правозащитных групп, самиздата, требований соблюдения конституционных прав [[5]][[11]].",
        year_range=(1965, 1980),
        tags=[EventTag.IDEOLOGY, EventTag.CRISIS, EventTag.SOCIAL],
        effects_accept={"stability": -5, "budget": -2, "support": -3, "ideology": -4},
        effects_reject={"stability": 3, "budget": 1, "support": 2, "ideology": 4},
        effects_compromise={"stability": -1, "budget": 0, "support": 0, "ideology": -1},
        min_stability=30.0
    ),
    
    # === СЕЛЬСКОЕ ХОЗЯЙСТВО ===
    "virgin_lands_1960s": HistoricalEvent(
        id="virgin_lands_1960s",
        title="Освоение целинных земель (завершающий этап)",
        description="Завершение программы распашки целины, оценка её эффективности и корректировка аграрной политики.",
        year_range=(1960, 1965),
        tags=[EventTag.AGRICULTURE, EventTag.ECONOMY],
        effects_accept={"stability": 2, "budget": -2, "support": 3, "ideology": 1},
        effects_reject={"stability": -3, "budget": 1, "support": -4, "ideology": 0},
        effects_compromise={"stability": 0, "budget": 0, "support": 0, "ideology": 0},
    ),
    
    "food_program_1980": HistoricalEvent(
        id="food_program_1980",
        title="Продовольственная программа",
        description="Комплекс мер по увеличению производства продуктов питания, развитие агропромышленного комплекса.",
        year_range=(1980, 1985),
        tags=[EventTag.AGRICULTURE, EventTag.SOCIAL],
        effects_accept={"stability": 4, "budget": -5, "support": 5, "ideology": 1},
        effects_reject={"stability": -5, "budget": 2, "support": -6, "ideology": 0},
        effects_compromise={"stability": 1, "budget": -2, "support": 2, "ideology": 0},
    ),
}

def get_available_events(year: int, stability: float, strategy: str) -> List[HistoricalEvent]:
    """Возвращает события, доступные в текущий момент"""
    available = []
    for evt in HISTORICAL_EVENTS.values():
        if (evt.year_range[0] <= year <= evt.year_range[1] and
            stability >= evt.min_stability and
            (evt.required_strategy is None or evt.required_strategy == strategy)):
            available.append(evt)
    return available