import copy

# DEFAULT_STATE должен содержать player_cc_id = None по умолчанию, если игрок не член ЦК изначально
DEFAULT_STATE = {
    "year": 1960,
    "month": 1,
    "turn": 0,
    "logs": ["☭ Система инициализирована."],
    "pending_effects": [],
    "player_cc_id": None, # <--- Должно быть None
    "career_level": "raykom",
    "career_score": 0.0,
    "career_reputation": 65.0,
    "career_incidents": 0,
    # ... (остальные поля из вашего txt.txt, включая новые)
    "obkom_unlocked": False,
    "clan_affinity": 50.0,
    "corruption_risk": 0.0,
    "plan_pressure": 1.0,
    "historical_phase": "thaw",
    "obkom_apparatus": None,
    "obkom_hero_cc_id": None,
    "obkom_bureau_tension": 40.0,
    "obkom_hero_ascent": 8.0,
    "political_capital": 40.0,
    "kgb_attention": 8.0,
    "obkom_secretariat": None,
    "secretariat_dilemma": None,
    "plenum_months_counter": 0,
    "regional_plenum_open": False,
    "regional_plenum_init1": None,
    "regional_plenum_init2": None,
    "regional_plenum_last_result": None,
    "petitions_queue": [],
    "career_growth_block_turns": 0,
    "obkom_hero_seated": False,
    # ... (остальные поля)
    "player_profile": None, # <--- Может быть None до создания
    "cc_members": None, # <--- Инициализируется в init_cc_data
    "regions": None, # <--- Инициализируется в init_cc_data
    "career": None, # <--- Инициализируется в character_creation
    # ... (остальные поля)
    "stability": 50.0,  # Добавлено поле 'stability'
    "budget": 1000.0,  # Добавлено поле 'budget'
    "support": None,  # Add the 'support' key
}

def get_clean_state():
    return copy.deepcopy(DEFAULT_STATE)

