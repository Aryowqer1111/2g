# data/regions_db.py
REGION_META = {
    # РСФСР — ключевые промышленные/политические центры
    "msk_obl": {"name": "Московская область", "type": "oblast", "parent": "rsfsr", "ind_weight": 0.22, "agri_weight": 0.05, "pol_influence": 0.95, "default_faction": "ideologues"},
    "len_obl": {"name": "Ленинградская область", "type": "oblast", "parent": "rsfsr", "ind_weight": 0.15, "agri_weight": 0.03, "pol_influence": 0.70, "default_faction": "reformers"},
    "sw_obl":  {"name": "Свердловская область", "type": "oblast", "parent": "rsfsr", "ind_weight": 0.12, "agri_weight": 0.04, "pol_influence": 0.60, "default_faction": "military"},
    "nsk_obl": {"name": "Новосибирская область", "type": "oblast", "parent": "rsfsr", "ind_weight": 0.08, "agri_weight": 0.06, "pol_influence": 0.45, "default_faction": "regions"},
    
    # Союзные республики (УССР, БССР, Казахстан, Узбекистан и др.)
    "ua_ssr":  {"name": "Украинская ССР", "type": "republic", "parent": "union", "ind_weight": 0.28, "agri_weight": 0.18, "pol_influence": 0.85, "default_faction": "regions"},
    "by_ssr":  {"name": "Белорусская ССР", "type": "republic", "parent": "union", "ind_weight": 0.06, "agri_weight": 0.10, "pol_influence": 0.55, "default_faction": "ideologues"},
    "kk_ssr":  {"name": "Казахская ССР", "type": "republic", "parent": "union", "ind_weight": 0.07, "agri_weight": 0.14, "pol_influence": 0.65, "default_faction": "regions"},
    "uz_ssr":  {"name": "Узбекская ССР", "type": "republic", "parent": "union", "ind_weight": 0.04, "agri_weight": 0.12, "pol_influence": 0.50, "default_faction": "regions"},
    "ge_ssr":  {"name": "Грузинская ССР", "type": "republic", "parent": "union", "ind_weight": 0.05, "agri_weight": 0.08, "pol_influence": 0.40, "default_faction": "reformers"},
    "am_ssr":  {"name": "Армянская ССР", "type": "republic", "parent": "union", "ind_weight": 0.03, "agri_weight": 0.06, "pol_influence": 0.30, "default_faction": "ideologues"},
    "az_ssr":  {"name": "Азербайджанская ССР", "type": "republic", "parent": "union", "ind_weight": 0.06, "agri_weight": 0.07, "pol_influence": 0.35, "default_faction": "reformers"},
    "lt_ssr":  {"name": "Литовская ССР", "type": "republic", "parent": "union", "ind_weight": 0.04, "agri_weight": 0.05, "pol_influence": 0.30, "default_faction": "ideologues"},
    "lv_ssr":  {"name": "Латвийская ССР", "type": "republic", "parent": "union", "ind_weight": 0.03, "agri_weight": 0.04, "pol_influence": 0.25, "default_faction": "ideologues"},
    "ee_ssr":  {"name": "Эстонская ССР", "type": "republic", "parent": "union", "ind_weight": 0.03, "agri_weight": 0.04, "pol_influence": 0.25, "default_faction": "reformers"},
    "md_ssr":  {"name": "Молдавская ССР", "type": "republic", "parent": "union", "ind_weight": 0.02, "agri_weight": 0.09, "pol_influence": 0.20, "default_faction": "regions"},
    "tj_ssr":  {"name": "Таджикская ССР", "type": "republic", "parent": "union", "ind_weight": 0.01, "agri_weight": 0.08, "pol_influence": 0.15, "default_faction": "regions"},
    "kg_ssr":  {"name": "Кыргызская ССР", "type": "republic", "parent": "union", "ind_weight": 0.01, "agri_weight": 0.06, "pol_influence": 0.15, "default_faction": "regions"}
}