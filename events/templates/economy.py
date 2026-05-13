from dataclasses import dataclass
from typing import List, Dict
from events.tags import EventTag

@dataclass
class AgendaTemplate:
    id: str
    title: str
    description: str
    tags: List[EventTag]
    choices: List[Dict]

ECONOMY_AGENDAS: List[AgendaTemplate] = [
    # === ПЛАНИРОВАНИЕ И ГОСПЛАН ===
    AgendaTemplate("plan_9_pyatiletka",
        "Утверждение директив IX пятилетки (1971–1975)",
        "Госплан представил основные направления развития народного хозяйства. Предусматривается ускоренный рост групп «Б» и повышение эффективности капитальных вложений.",
        [EventTag.ECONOMY],
        [
            {"text": "Утвердить в полном объёме", "effects": {"stability": 2, "budget": -3, "support": 3, "ideology": 1}},
            {"text": "Скорректировать в пользу потребительского сектора", "effects": {"stability": 1, "budget": -2, "support": 5, "ideology": -2}},
            {"text": "Вернуть на доработку с учётом ресурсных ограничений", "effects": {"stability": -1, "budget": 1, "support": 0, "ideology": 0}}
        ]),
    AgendaTemplate("plan_val_output",
        "О замене показателя «валовая продукция» на «реализованную продукцию»",
        "Минфин и Госплан предлагают устранить стимулы к производству невостребованных товаров. Переход потребует пересмотра нормативов и фондов.",
        [EventTag.ECONOMY],
        [
            {"text": "Внедрить показатель повсеместно", "effects": {"stability": 2, "budget": 2, "support": 2, "ideology": -1}},
            {"text": "Провести эксперимент на 50 предприятиях", "effects": {"stability": 0, "budget": 0, "support": 1, "ideology": 0}},
            {"text": "Сохранить валовые показатели как базовые", "effects": {"stability": 0, "budget": -1, "support": -2, "ideology": 2}}
        ]),

    # === СЕЛЬСКОЕ ХОЗЯЙСТВО И ПРОДОВОЛЬСТВИЕ ===
    AgendaTemplate("agro_grain_1963",
        "О состоянии хлебных ресурсов и закупках зерна за рубежом",
        "Неурожай в Поволжье и на Урале создал дефицит фуражного и продовольственного зерна. Требуется санкционирование валютных ассигнований на импорт.",
        [EventTag.ECONOMY, EventTag.AGRICULTURE, EventTag.FOREIGN],
        [
            {"text": "Разрешить закупки в Канаде и США", "effects": {"stability": 3, "budget": -4, "support": 4, "ideology": -3}},
            {"text": "Ввести карточную систему в ряде регионов", "effects": {"stability": -3, "budget": 0, "support": -5, "ideology": 1}},
            {"text": "Мобилизовать резервы и ужесточить нормирование", "effects": {"stability": -1, "budget": -1, "support": -2, "ideology": 2}}
        ]),
    AgendaTemplate("agro_nechernozeme",
        "О развитии мелиорации и освоении Нечерноземья",
        "Принята масштабная программа подъёма сельского хозяйства в центральных и северных областях. Требуется утверждение лимитов на технику и удобрения.",
        [EventTag.ECONOMY, EventTag.AGRICULTURE],
        [
            {"text": "Утвердить программу с полным финансированием", "effects": {"stability": 2, "budget": -5, "support": 3, "ideology": 1}},
            {"text": "Сократить объёмы до пилотных зон", "effects": {"stability": 0, "budget": 2, "support": 0, "ideology": 0}},
            {"text": "Перенаправить средства на целину", "effects": {"stability": 1, "budget": -2, "support": -1, "ideology": 2}}
        ]),
    AgendaTemplate("agro_food_prog_1982",
        "О реализации Продовольственной программы 1982 года",
        "Комплекс мер по увеличению производства мяса, молока, овощей и фруктов. Предусматривается создание агропромышленных объединений.",
        [EventTag.ECONOMY, EventTag.AGRICULTURE, EventTag.SOCIAL],
        [
            {"text": "Утвердить программу целиком", "effects": {"stability": 3, "budget": -6, "support": 6, "ideology": 1}},
            {"text": "Ограничить развитие личных подсобных хозяйств", "effects": {"stability": 1, "budget": -3, "support": 2, "ideology": 4}},
            {"text": "Разрешить арендные отношения в колхозах", "effects": {"stability": 2, "budget": -4, "support": 5, "ideology": -4}}
        ]),

    # === ПРОМЫШЛЕННОСТЬ И ТЯЖМАШ ===
    AgendaTemplate("ind_kosygin_reform",
        "О переводе предприятий на хозрасчёт и самофинансирование",
        "Реформа 1965 года расширяет самостоятельность заводов. Директора получают право формировать фонды развития и материального стимулирования.",
        [EventTag.ECONOMY, EventTag.CADRES],
        [
            {"text": "Распространить на все отрасли", "effects": {"stability": 3, "budget": 1, "support": 4, "ideology": -3}},
            {"text": "Ограничить реформу машиностроением", "effects": {"stability": 1, "budget": 0, "support": 1, "ideology": -1}},
            {"text": "Вернуться к жёсткому централизованному планированию", "effects": {"stability": -2, "budget": -2, "support": -3, "ideology": 4}}
        ]),
    AgendaTemplate("ind_chemical_push",
        "Об ускоренном развитии химической промышленности",
        "Постановление о создании новых мощностей по производству минеральных удобрений, синтетических волокон и пластмасс. Требуется увеличение капвложений.",
        [EventTag.ECONOMY, EventTag.SCIENCE],
        [
            {"text": "Утвердить строительство 12 новых комбинатов", "effects": {"stability": 2, "budget": -5, "support": 3, "ideology": 0}},
            {"text": "Модернизировать существующие предприятия", "effects": {"stability": 1, "budget": -2, "support": 1, "ideology": 0}},
            {"text": "Отложить реализацию в пользу ВПК", "effects": {"stability": 0, "budget": 3, "support": -1, "ideology": 3}}
        ]),
    AgendaTemplate("ind_machine_tools",
        "О состоянии станкостроения и приборостроения",
        "Отмечается отставание в выпуске ЧПУ и высокоточного оборудования. Требуется переориентация НИИ и заводов на микроэлектронную компонентную базу.",
        [EventTag.ECONOMY, EventTag.SCIENCE],
        [
            {"text": "Создать межотраслевой научно-производственный комплекс", "effects": {"stability": 2, "budget": -4, "support": 2, "ideology": -1}},
            {"text": "Закупить лицензии у западных фирм", "effects": {"stability": 1, "budget": -3, "support": 1, "ideology": -3}},
            {"text": "Сохранить текущие темпы модернизации", "effects": {"stability": 0, "budget": 0, "support": 0, "ideology": 1}}
        ]),

    # === ЭНЕРГЕТИКА И РЕСУРСЫ ===
    AgendaTemplate("energy_siberia_oil",
        "Об освоении нефтегазовых месторождений Западной Сибири",
        "Самотлор, Уренгой, Ямал требуют масштабных капиталовложений, трубопроводов и вахтовых посёлков. Прогнозируется кратный рост экспортных возможностей.",
        [EventTag.ECONOMY, EventTag.FOREIGN],
        [
            {"text": "Придать проекту статус всенародной стройки", "effects": {"stability": 4, "budget": -7, "support": 5, "ideology": 2}},
            {"text": "Осваивать поэтапно с привлечением иностранных кредитов", "effects": {"stability": 2, "budget": -4, "support": 2, "ideology": -2}},
            {"text": "Сосредоточиться на Поволжье и Баку", "effects": {"stability": 0, "budget": 2, "support": -1, "ideology": 1}}
        ]),
    AgendaTemplate("energy_nuclear",
        "О расширении программы строительства атомных электростанций",
        "АЭС позволяют снизить зависимость от органического топлива. Требуется утверждение площадок, кадрового обеспечения и мер радиационной безопасности.",
        [EventTag.ECONOMY, EventTag.SCIENCE],
        [
            {"text": "Утвердить строительство 10 блоков ВВЭР", "effects": {"stability": 2, "budget": -6, "support": 3, "ideology": 0}},
            {"text": "Развивать только тепловую и гидрогенерацию", "effects": {"stability": 0, "budget": 1, "support": 0, "ideology": 2}},
            {"text": "Заморозить программу до отработки технологии", "effects": {"stability": 0, "budget": 2, "support": -1, "ideology": 1}}
        ]),

    # === ПОТРЕБИТЕЛЬСКИЙ СЕКТОР И ДЕФИЦИТ ===
    AgendaTemplate("consumer_goods_push",
        "О расширении производства товаров народного потребления",
        "Розничная торговля испытывает дефицит обуви, тканей, бытовой техники. Легпром запрашивает перераспределение сырья и станков из группы «А».",
        [EventTag.ECONOMY, EventTag.SOCIAL],
        [
            {"text": "Перенаправить 15% ресурсов в группу «Б»", "effects": {"stability": 4, "budget": -3, "support": 7, "ideology": -2}},
            {"text": "Увеличить импорт готовых изделий", "effects": {"stability": 2, "budget": -4, "support": 3, "ideology": -3}},
            {"text": "Сохранить приоритет тяжёлой промышленности", "effects": {"stability": -2, "budget": 2, "support": -4, "ideology": 3}}
        ]),
    AgendaTemplate("consumer_coupons_1990",
        "О введении талонов на отдельные виды продовольствия и промтоваров",
        "Рост денежной массы при неизменном товарном предложении требует нормирования потребления для предотвращения ажиотажного спроса.",
        [EventTag.ECONOMY, EventTag.CRISIS, EventTag.SOCIAL],
        [
            {"text": "Ввести талоны на сахар, мясо, мыло", "effects": {"stability": -2, "budget": 1, "support": -6, "ideology": 0}},
            {"text": "Повысить розничные цены на 30%", "effects": {"stability": -4, "budget": 3, "support": -7, "ideology": -1}},
            {"text": "Разрешить свободную продажу через кооперативы", "effects": {"stability": 1, "budget": 2, "support": 2, "ideology": -4}}
        ]),

    # === ВНЕШНЯЯ ТОРГОВЛЯ И ЗАДОЛЖЕННОСТЬ ===
    AgendaTemplate("trade_comecon",
        "О расширении внешнеторговых связей со странами СЭВ",
        "Предлагается углубить специализацию производства, перейти на расчёты в переводных рублях, создать совместные научно-технические центры.",
        [EventTag.ECONOMY, EventTag.SOCIALIST_BLOC],
        [
            {"text": "Утвердить программу интеграции", "effects": {"stability": 2, "budget": -1, "support": 2, "ideology": 2}},
            {"text": "Ограничиться поставками сырья в обмен на оборудование", "effects": {"stability": 0, "budget": 1, "support": 0, "ideology": 0}},
            {"text": "Свернуть торговлю в пользу расчётов в конвертабельной валюте", "effects": {"stability": 1, "budget": -3, "support": -1, "ideology": -2}}
        ]),
    AgendaTemplate("trade_western_loans",
        "О привлечении западных кредитов под закупку промышленных линий",
        "Европейские банки предлагают долгосрочные займы под 4–6% годовых. Средства пойдут на модернизацию химпрома, металлургии и транспорта.",
        [EventTag.ECONOMY, EventTag.FOREIGN],
        [
            {"text": "Привлечь кредиты на $2 млрд", "effects": {"stability": 2, "budget": 3, "support": 1, "ideology": -2}},
            {"text": "Ограничиться бартерными сделками", "effects": {"stability": 0, "budget": 0, "support": 0, "ideology": 1}},
            {"text": "Отказаться от займов во избежание долговой зависимости", "effects": {"stability": 1, "budget": -2, "support": 2, "ideology": 3}}
        ]),

    # === ПЕРЕСТРОЙКА И РЫНОЧНЫЕ РЕФОРМЫ (1985–1991) ===
    AgendaTemplate("perestroika_enterprise_law",
        "О Законе о государственном предприятии (1987)",
        "Предприятия переходят на полный хозрасчёт, самофинансирование и самоуправление. Трудовые коллективы получают право избирать директоров.",
        [EventTag.ECONOMY, EventTag.CADRES],
        [
            {"text": "Внедрить закон без ограничений", "effects": {"stability": 1, "budget": 2, "support": 4, "ideology": -5}},
            {"text": "Сохранить госзаказ на 70% продукции", "effects": {"stability": 2, "budget": 0, "support": 1, "ideology": -2}},
            {"text": "Отложить реформу до стабилизации цен", "effects": {"stability": 0, "budget": -1, "support": 0, "ideology": 3}}
        ]),
    AgendaTemplate("perestroika_cooperatives",
        "О развитии кооперативного движения в сфере услуг и производства",
        "Легализация частного предпринимательства в форме кооперативов. Требуется утверждение налоговых ставок и мер контроля за ценообразованием.",
        [EventTag.ECONOMY, EventTag.SOCIAL],
        [
            {"text": "Разрешить кооперативы с налогом 40%", "effects": {"stability": 2, "budget": 3, "support": 3, "ideology": -4}},
            {"text": "Ограничить деятельность бытовыми услугами", "effects": {"stability": 1, "budget": 1, "support": 0, "ideology": -1}},
            {"text": "Запретить как проявление мелкобуржуазной стихии", "effects": {"stability": -2, "budget": -2, "support": -3, "ideology": 5}}
        ]),
    AgendaTemplate("perestroika_pavlov_reform",
        "О проведении денежной реформы и обмене крупных купюр (1991)",
        "Изъятие из обращения банкнот 50 и 100 рублей образца 1961 года. Ограничение сроков обмена и сумм для граждан.",
        [EventTag.ECONOMY, EventTag.CRISIS],
        [
            {"text": "Провести обмен с жёсткими лимитами", "effects": {"stability": -5, "budget": 4, "support": -8, "ideology": 0}},
            {"text": "Ограничиться конфискацией у теневиков", "effects": {"stability": -1, "budget": 1, "support": 2, "ideology": 1}},
            {"text": "Отменить реформу и выпустить новые купюры позже", "effects": {"stability": 2, "budget": -3, "support": 3, "ideology": -1}}
        ]),

    # === ИНФРАСТРУКТУРА И СТРОИТЕЛЬСТВО ===
    AgendaTemplate("infra_bam_construction",
        "О строительстве Байкало-Амурской магистрали",
        "БАМ обеспечит доступ к месторождениям Восточной Сибири и Дальнего Востока. Требуется мобилизация комсомольских ресурсов и техники.",
        [EventTag.ECONOMY, EventTag.SOCIAL],
        [
            {"text": "Утвердить ударную стройку с льготами участникам", "effects": {"stability": 3, "budget": -8, "support": 5, "ideology": 3}},
            {"text": "Строить поэтапно в мирном режиме", "effects": {"stability": 1, "budget": -4, "support": 2, "ideology": 0}},
            {"text": "Перенаправить средства на БАТ (Байкало-Амурский тоннель)", "effects": {"stability": 0, "budget": -2, "support": 0, "ideology": 1}}
        ]),
    AgendaTemplate("infra_housing_khrushchev",
        "О массовом индустриальном жилищном строительстве",
        "Переход к панельному домостроению позволит ликвидировать коммунальное заселение за 10–12 лет. Требуется создание домостроительных комбинатов.",
        [EventTag.ECONOMY, EventTag.SOCIAL],
        [
            {"text": "Утвердить типовые серии и ускорить сроки", "effects": {"stability": 4, "budget": -5, "support": 8, "ideology": 0}},
            {"text": "Сохранить индивидуальное проектирование", "effects": {"stability": 0, "budget": -2, "support": 1, "ideology": 2}},
            {"text": "Сократить объёмы в пользу промышленности", "effects": {"stability": -3, "budget": 3, "support": -4, "ideology": 3}}
        ]),

    # === КРИЗИС, ТЕНЕВАЯ ЭКОНОМИКА И СТАГНАЦИЯ ===
    AgendaTemplate("crisis_budget_deficit",
        "О ликвидации дефицита госбюджета и сокращении расходов",
        "Рост дотаций предприятиям и военные расходы создают хронический дефицит. Минфин предлагает сократить капвложения и субсидии.",
        [EventTag.ECONOMY, EventTag.CRISIS],
        [
            {"text": "Сократить дотации нерентабельным заводам", "effects": {"stability": 1, "budget": 5, "support": -4, "ideology": -1}},
            {"text": "Ввести акцизы на алкоголь и табак", "effects": {"stability": -1, "budget": 4, "support": -5, "ideology": 0}},
            {"text": "Покрыть дефицит за счёт эмиссии", "effects": {"stability": 0, "budget": 2, "support": -2, "ideology": -2}}
        ]),
    AgendaTemplate("crisis_shadow_economy",
        "О борьбе с нетрудовыми доходами и теневой экономикой",
        "Спекуляция, цеховики, махинации с госимуществом подрывают плановую систему. Требуется усиление контроля и ужесточение наказаний.",
        [EventTag.ECONOMY, EventTag.CRISIS, EventTag.CADRES],
        [
            {"text": "Создать спецкомиссии при МВД и КГБ", "effects": {"stability": 2, "budget": 2, "support": -3, "ideology": 4}},
            {"text": "Легализовать часть деятельности через кооперативы", "effects": {"stability": 1, "budget": 3, "support": 1, "ideology": -3}},
            {"text": "Игнорировать как временное явление", "effects": {"stability": -2, "budget": -1, "support": 0, "ideology": 0}}
        ]),
]