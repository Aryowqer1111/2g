# data/leaders.py

LEADERS_DB = {
    "khrushchev": {
        "name": "Никита Сергеевич Хрущёв",
        "start_year": 1953,
        "end_year": 1964,
        "stats": {
            "authority": 85,      # Влияние в партии
            "reformism": 90,      # Склонность к реформам
            "stability_focus": 40 # Внимание к стабильности
        },
        "bonuses": {
            "agriculture": 1.2,   # Бонус к сельскому хозяйству (Целина)
            "military": 0.9       # Штраф к ВПК (сокращение армии)
        }
    },
    "brezhnev": {
        "name": "Леонид Ильич Брежнев",
        "start_year": 1964,
        "end_year": 1982,
        "stats": {
            "authority": 75,
            "reformism": 20,
            "stability_focus": 95
        },
        "bonuses": {
            "military": 1.3,      # Бонус к ВПК (Разрядка и гонка вооружений)
            "ideology": 1.1       # Усиление цензуры
        }
    },
    "kosygin": {
        "name": "Алексей Николаевич Косыгин",
        "role": "Председатель Совмина",
        "stats": {
            "authority": 70,
            "reformism": 95,      # Реформа 1965 года
            "economy_skill": 90
        }
    }
}

FACTIONS_DB = {
    "ideologues": {"name": "Идеологи", "leader": "М. Суслов", "base_influence": 60},
    "reformers": {"name": "Реформаторы", "leader": "А. Косыгин", "base_influence": 45},
    "military": {"name": "ВПК / Силовики", "leader": "Д. Устинов", "base_influence": 70},
    "regions": {"name": "Региональные элиты", "leader": "Л. Брежнев", "base_influence": 50}
}