# data/events_db.py

EVENTS_POOL = [
    {
        "id": "evt_corn_crisis",
        "title": "🌽 Кукурузная лихорадка",
        "text": "Хрущёв требует повсеместного внедрения кукурузы. Агрономы предупреждают, что климат не подходит.",
        "year_min": 1960,
        "year_max": 1964,
        "choices": [
            {"text": "Поддержать Генсека", "effects": {"support": -5, "agriculture": 10, "stability": -2}},
            {"text": "Саботировать указания", "effects": {"support": 2, "agriculture": -5, "authority_leader": -5}},
            {"text": "Найти компромисс", "effects": {"support": 0, "agriculture": 2}}
        ]
    },
    {
        "id": "evt_novocherkassk",
        "title": "⚠️ Новочеркасск",
        "text": "Рабочие вышли на протест из-за повышения цен на мясо и масло. Ситуация накаляется.",
        "year_min": 1962,
        "year_max": 1962,
        "choices": [
            {"text": "Жёсткое подавление (КГБ)", "effects": {"stability": -15, "support": -20, "authority_kgb": 10}},
            {"text": "Пойти на уступки", "effects": {"budget": -10, "support": 10, "stability": 5}},
            {"text": "Игнорировать", "effects": {"stability": -30, "support": -10}}
        ]
    },
    {
        "id": "evt_space_race",
        "title": "🚀 Гагарин в космосе",
        "text": "СССР первым отправил человека в космос! Весь мир в восторге.",
        "year_min": 1961,
        "year_max": 1961,
        "choices": [
            {"text": "Увеличить финансирование ВПК", "effects": {"prestige": 20, "budget": -15, "military_tech": 10}},
            {"text": "Использовать успех в пропаганде", "effects": {"prestige": 15, "ideology": 5}}
        ]
    },
    {
        "id": "evt_oil_discovery",
        "title": "🛢 Нефть Западной Сибири",
        "text": "Обнаружены гигантские месторождения в Тюменской области.",
        "year_min": 1965,
        "year_max": 1970,
        "choices": [
            {"text": "Инвестировать в разработку", "effects": {"budget_long_term": 50, "budget_short_term": -20}},
            {"text": "Продать лицензии на Запад", "effects": {"budget": 10, "relations_west": 5}}
        ]
    }
]