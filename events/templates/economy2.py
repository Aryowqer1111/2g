from dataclasses import dataclass
from typing import List, Dict
from events.tags import EventTag

@dataclass
class DynamicAgenda:
    id: str
    title: str
    description: str
    tags: List[EventTag]
    choices: List[Dict]
    condition: str = "neutral"  # success, crisis, neutral

DYNAMIC_ECONOMY_AGENDAS: List[DynamicAgenda] = [
    # 🔹 УСПЕХИ
    DynamicAgenda("dyn_overfulfillment", "Перевыполнение плана в машиностроении",
                  "Ведущие заводы отчитались о превышении квартальных норм на 15–20%. Требуется решение о премировании и распределении сверхплановой продукции.",
                  [EventTag.ECONOMY, EventTag.CADRES],
                  [{"text": "Утвердить премии и почётные грамоты", "effects": {"stability": 2, "budget": -1, "support": 4}},
                   {"text": "Направить излишки на экспорт", "effects": {"stability": 1, "budget": 3, "support": 0}},
                   {"text": "Повысить плановые показатели на следующий квартал", "effects": {"stability": -1, "budget": 2, "support": -2}}], "success"),

    DynamicAgenda("dyn_innovation", "Внедрение автоматизированной системы управления (АСУ)",
                  "Пилотный проект на текстильном комбинате сократил издержки на 12%. Минлегпром предлагает масштабировать опыт на отрасль.",
                  [EventTag.ECONOMY, EventTag.SCIENCE],
                  [{"text": "Утвердить тиражирование АСУ", "effects": {"stability": 2, "budget": -4, "support": 2, "ideology": -1}},
                   {"text": "Ограничить эксперимент одной областью", "effects": {"stability": 1, "budget": -1, "support": 1, "ideology": 0}},
                   {"text": "Отложить до завершения текущей пятилетки", "effects": {"stability": 0, "budget": 2, "support": -1, "ideology": 2}}], "success"),

    DynamicAgenda("dyn_export_windfall", "Неожиданный рост валютных поступлений от экспорта",
                  "Благоприятная конъюнктура на мировых рынках позволила реализовать сверхплановые объёмы нефти и газа. Минфин запрашивает решение о резервировании средств.",
                  [EventTag.ECONOMY, EventTag.FOREIGN],
                  [{"text": "Направить на закупку продовольствия", "effects": {"stability": 3, "budget": 2, "support": 5, "ideology": -2}},
                   {"text": "Пополнить золотовалютный резерв", "effects": {"stability": 2, "budget": 4, "support": 0, "ideology": 0}},
                   {"text": "Инвестировать в лёгкую промышленность", "effects": {"stability": 1, "budget": 0, "support": 3, "ideology": -3}}], "success"),

    # 🔹 НЕЙТРАЛЬНЫЕ / ТИПОВЫЕ
    DynamicAgenda("dyn_norm_delivery", "Срыв графиков поставок комплектующих",
                  "Смежные предприятия задерживают отгрузку узлов на 10–14 дней. Госплан предлагает ввести штрафные санкции или временную ручную диспетчеризацию.",
                  [EventTag.ECONOMY],
                  [{"text": "Ввести штрафные санкции по договору", "effects": {"stability": 0, "budget": 1, "support": -1}},
                   {"text": "Организовать ручную координацию", "effects": {"stability": 1, "budget": -2, "support": 2}},
                   {"text": "Разрешить взаимозачёты между ведомствами", "effects": {"stability": 0, "budget": 0, "support": 1}}], "neutral"),

    DynamicAgenda("dyn_labor_shortage", "Дефицит кадров на новостройках",
                  "Комсомольские отряды не полностью укомплектованы. Минстрой просит разрешить целевой набор из сельских районов или увеличить лимиты на вахтовый метод.",
                  [EventTag.ECONOMY, EventTag.SOCIAL, EventTag.CADRES],
                  [{"text": "Утвердить целевой набор с жилищными льготами", "effects": {"stability": 2, "budget": -3, "support": 3}},
                   {"text": "Перенаправить механизированные колонны", "effects": {"stability": 0, "budget": -1, "support": 0}},
                   {"text": "Скорректировать сроки сдачи объектов", "effects": {"stability": -2, "budget": 2, "support": -2}}], "neutral"),

    # 🔹 КРИЗИСЫ / ПРОБЛЕМЫ
    DynamicAgenda("dyn_shortage_parts", "Острая нехватка запасных частей и тормозных колодок",
                  "Железнодорожные узлы испытывают срыв графика перевозок из-за износа подвижного состава. Требуется экстренное решение по лимитам.",
                  [EventTag.ECONOMY, EventTag.CRISIS],
                  [{"text": "Выделить резервный фонд Госплана", "effects": {"stability": 2, "budget": -3, "support": 2}},
                   {"text": "Ввести режим жёсткой экономии и нормирования", "effects": {"stability": 0, "budget": 2, "support": -3}},
                   {"text": "Перераспределить поставки с других отраслей", "effects": {"stability": -1, "budget": 0, "support": -1}}], "crisis"),

    DynamicAgenda("dyn_inflation_shadow", "Рост спекулятивных цен на кооперативных рынках",
                  "Отмечается ажиотажный спрос и перепродажа промтоваров через кооперативы. Минфин предлагает ужесточить налоговый контроль или ввести ценовые лимиты.",
                  [EventTag.ECONOMY, EventTag.CRISIS, EventTag.SOCIAL],
                  [{"text": "Ввести предельные розничные наценки", "effects": {"stability": 1, "budget": 1, "support": -4, "ideology": 3}},
                   {"text": "Усилить проверки через финансовые органы", "effects": {"stability": 2, "budget": 2, "support": -2, "ideology": 2}},
                   {"text": "Легализовать часть операций через биржи", "effects": {"stability": -1, "budget": 3, "support": 1, "ideology": -4}}], "crisis"),

    DynamicAgenda("dyn_energy_crisis", "Веерные отключения электроэнергии в промышленных зонах",
                  "Из-за низкого уровня водохранилищ и задержек поставок угля ряд предприятий переведено на двухсменный график. Требуется утверждение графика приоритетных потребителей.",
                  [EventTag.ECONOMY, EventTag.CRISIS],
                  [{"text": "Составить жёсткий график приоритетов", "effects": {"stability": 0, "budget": 1, "support": -3}},
                   {"text": "Закупить уголь у союзных республик в кредит", "effects": {"stability": 2, "budget": -2, "support": 1}},
                   {"text": "Временный перевод на ручной труд в лёгкой промышленности", "effects": {"stability": -2, "budget": 0, "support": -4}}], "crisis"),
]