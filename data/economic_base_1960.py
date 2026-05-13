# data/economic_base_1960.py
# Базовые показатели и исторические значения для начала симуляции (1960 г.)
# Масштаб значений подобран так, чтобы 100 == Полный план

RESOURCE_CATALOG = {
    
    # 🔥 ТОПЛИВНО-ЭНЕРГЕТИЧЕСКИЙ КОМПЛЕКС (ТЭК) — Основа экономики
    "fuel_energy": {
        "oil_raw": {
            "name": "Сырая нефть",
            "current": 95.0,       # Около 95 млн тонн (реальный рост с середины 50-х)
            "plan": 105.0,         # План семилетки требовал бурного роста
            "unit": "млн тонн",
            "strategic_importance": 9.5, # Главный экспортный ресурс для валюты
            "ministry": "MinEnergo"
        },
        "gas": {
            "name": "Природный газ",
            "current": 50.0,       # Начало освоения Западной Сибири еще впереди, база Волга-Урал
            "plan": 58.0,
            "unit": "млрд м³",
            "strategic_importance": 7.0,
            "ministry": "MinEnergo"
        },
        "coal": {
            "name": "Уголь",
            "current": 460.0,      # СССР — лидер по добыче угля в мире
            "plan": 480.0,
            "unit": "млн тонн",
            "strategic_importance": 8.5,
            "ministry": "MinUgol"
        },
        "electricity": {
            "name": "Электроэнергия",
            "current": 320.0,      # Млрд кВт·ч (быстрый рост атомных и ГЭС)
            "plan": 350.0,
            "unit": "млрд кВт·ч",
            "strategic_importance": 9.0,
            "ministry": "MinEnergo"
        }
    },

    # ⛏️ ГОРНОДОБЫВАЮЩАЯ И МЕТАЛЛУРГИЧЕСКАЯ ОТРАСЛЬ — Сила государства
    "mining_metallurgy": {
        "steel": {
            "name": "Сталь",
            "current": 59.0,       # ~59 млн тонн (лидер в мире)
            "plan": 62.0,
            "unit": "млн тонн",
            "strategic_importance": 9.0, # Основа ВПК и машиностроения
            "ministry": "MinTyazhProm"
        },
        "copper": {
            "name": "Медь",
            "current": 850.0,      # Тонны (критична для электроники и ВПК)
            "plan": 880.0,
            "unit": "тыс тонн",
            "strategic_importance": 7.5,
            "ministry": "MinTsvetMet"
        },
        "aluminum": {
            "name": "Алюминий",
            "current": 600.0,      # Критичен для авиации и космоса
            "plan": 630.0,
            "unit": "тыс тонн",
            "strategic_importance": 8.0,
            "ministry": "MinTsvetMet"
        },
        "chemicals": {
            "name": "Промышленная химия", # Удобрения, волокна
            "current": 45.0,       # Хрущевское "Химизация народного хозяйства"
            "plan": 55.0,          # Высокий план развития
            "unit": "млн тонн (условно)",
            "strategic_importance": 6.5,
            "ministry": "MinKhimprom"
        }
    },

    # 🌾 АГРОПРОМЫШЛЕННЫЙ КОМПЛЕКС (АПК) — Индекс стабильности
    "agriculture": {
        "grain": {
            "name": "Зерно", # Пшеница, кукуруза
            "current": 125.0,      # После рекорда 1958 года начался спад
            "plan": 135.0,         # Амбициозные цели сева
            "unit": "млн тонн",
            "strategic_importance": 9.5, # От этого зависит Поддержка населения напрямую
            "weather_sensitivity": True # Флаг зависимости от рандома (погода)
        },
        "meat_dairy": {
            "name": "Мясо и молоко",
            "current": 60.0,       # Тысячи тонн (продукты питания дефицитны)
            "plan": 68.0,
            "unit": "тыс тонн",
            "strategic_importance": 9.0, # Прямой драйвер индекса "Поддержка"
            "ministry": "MinSelkhoz"
        },
        "cotton": {
            "name": "Хлопок",
            "current": 350.0,      # Средняя Азия — грабли Хрущева
            "plan": 380.0,
            "unit": "тыс тонн",
            "strategic_importance": 6.0,
            "ministry": "MinSelkhoz"
        }
    },

    # 🏗 СТРОИТЕЛЬСТВО И МАШИНОСТРОЕНИЕ
    "construction_industry": {
        "cement_bricks": {
            "name": "Цемент и кирпич",
            "current": 35.0,       # Строительный бум хрущевских панельок
            "plan": 40.0,
            "unit": "млн условных ед.",
            "strategic_importance": 7.0,
            "ministry": "Mingospromstroy"
        },
        "machinery_trucks": {
            "name": "Грузовики и тракторы",
            "current": 300.0,      # Тысячи единиц
            "plan": 320.0,
            "unit": "тыс шт",
            "strategic_importance": 8.5, # Обеспечивает все остальные отрасли транспортом
            "ministry": "MinTraktormash"
        },
        
        "construction_materials": {
            "name": "Стройматериалы (общее)",
            "current": 55.0,
            "plan": 60.0,
            "unit": "% к плану",
            "strategic_importance": 7.5,
            "ministry": "Mingospromstroy"
        }
    },

    # 💰 ФИНАНСЫ И ТОРГОВЛЯ
    "finance_trade": {
        "gold_reserves": {
            "name": "Золотой запас",
            "current": 100.0,      # Индекс прочности валюты
            "plan": 100.0,
            "unit": "тонн (условно)",
            "strategic_importance": 9.0
        },
        "soft_goods_stock": {
            "name": "Запас товаров народного потребления",
            "current": 45.0,       # Магазы пусты — главный источник недовольства
            "plan": 55.0,
            "unit": "млрд руб (опт)",
            "strategic_importance": 8.0,
            "ministry": "MinTorg"
        },
        "budget_revenue": {
            "name": "Доходы бюджета",
            "current": 80.0,       # % выполнения плана доходов
            "plan": 100.0,
            "unit": "% плана",
            "strategic_importance": 9.5
        }
    }
}