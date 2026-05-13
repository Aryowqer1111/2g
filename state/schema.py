import copy
DEFAULT_STATE = {
    "year": 1960, "month": 1, "turn": 0,
    "logs": ["☭ Система инициализирована."], "pending_effects": [],
    "player_cc_id": None, "career_level": "raykom", "career_score": 0.0,
    "career_reputation": 65.0, "career_incidents": 0,
    "faction_coalitions": {}, "plenum_agenda": [], "congress_next_year": 1961,
    "politburo_ids": [], "gen_sec_authority": 85.0,
    "gdp_index": 100.0, "budget": 50.0, "inflation_hidden": 0.0,
    "ministry_efficiency": {}, "five_year_plan": {"progress": 0.0, "deadline": 1965, "target": 105.0},
    "reform_policy": "centralized", "reform_intensity": 0.0, "economic_model": "soviet_standard",
    "tech_branches": {"space": 50, "nuclear": 60, "computing": 30},
    "shadow_economy": 0.0, "corruption_index": 15.0,
    "relations_usa": -60.0, "relations_warsaw_pact": 80.0, "relations_nam": 40.0,
    "sev_integration": 70.0, "crisis_active": None,
    "military_industry": {"conventional": 80, "nuclear": 40, "space": 50},
    "thaw_index": 70.0, "ideology_rigidness": 50.0, "intelligentsia_mood": 65.0, "cultural_freedom": 60.0,
    "regional_nationalism": {"ua": 10, "kk": 15, "caucasus": 20}, "repression_level": 20.0,
    "ui_metrics_history": [], "advisors_active": True, "ai_events_enabled": False,
    "cc_selected_id": None, "selected_committee": None, "character_created": False,
    "stability": 70.0, "support": 65.0, "ideology": 70.0, "prestige": 60.0, "security": 65.0,
    "cc_members": None, "regions": None, "career": None, "player_profile": None
}
def get_clean_state(): return copy.deepcopy(DEFAULT_STATE)