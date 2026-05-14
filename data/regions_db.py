# 🔹 НОВОЕ: плоская иерархия — parent_republic, type: republic | oblast | raikom
# РСФСР: республика + 8 крупных областей; союзные республики — по 3–4 обкома/области.

def _r(name, rtype, parent_republic, ind, agri, pol, faction):
    return {
        "name": name,
        "type": rtype,
        "parent_republic": parent_republic,
        "ind_weight": ind,
        "agri_weight": agri,
        "pol_influence": pol,
        "default_faction": faction,
    }


REGION_META = {
    # --- РСФСР (союзная республика в составе СССР) ---
    "rsfsr": _r("РСФСР (агрегат)", "republic", "union", 0.55, 0.22, 0.92, "ideologues"),
    "rsfsr_msk_obl": _r("Московская область", "oblast", "rsfsr", 0.20, 0.05, 0.95, "ideologues"),
    "rsfsr_len_obl": _r("Ленинградская область", "oblast", "rsfsr", 0.14, 0.03, 0.72, "reformers"),
    "rsfsr_sve_obl": _r("Свердловская область", "oblast", "rsfsr", 0.11, 0.04, 0.62, "ВПК"),
    "rsfsr_nsk_obl": _r("Новосибирская область", "oblast", "rsfsr", 0.08, 0.06, 0.48, "Регионы"),
    "rsfsr_rst_obl": _r("Ростовская область", "oblast", "rsfsr", 0.09, 0.10, 0.52, "Регионы"),
    "rsfsr_krd_krai": _r("Краснодарский край", "oblast", "rsfsr", 0.08, 0.12, 0.50, "Регионы"),
    "rsfsr_perm_obl": _r("Пермская область", "oblast", "rsfsr", 0.10, 0.05, 0.44, "ВПК"),
    "rsfsr_khb_krai": _r("Хабаровский край", "oblast", "rsfsr", 0.07, 0.04, 0.46, "ВПК"),
    "rsfsr_tula_raikom": _r("Тульский райком (узел)", "raikom", "rsfsr", 0.04, 0.06, 0.35, "Идеологи"),
    # --- УССР ---
    "ua_ssr": _r("Украинская ССР", "republic", "union", 0.26, 0.18, 0.86, "Регионы"),
    "ua_kharkiv_obl": _r("Харьковская область", "oblast", "ua_ssr", 0.12, 0.10, 0.58, "ВПК"),
    "ua_odessa_obl": _r("Одесская область", "oblast", "ua_ssr", 0.08, 0.11, 0.52, "Регионы"),
    "ua_dnipropetrovsk_obl": _r("Днепропетровская область", "oblast", "ua_ssr", 0.14, 0.07, 0.62, "ВПК"),
    "ua_lviv_obl": _r("Львовская область", "oblast", "ua_ssr", 0.06, 0.08, 0.42, "Реформаторы"),
    # --- БССР ---
    "by_ssr": _r("Белорусская ССР", "republic", "union", 0.07, 0.11, 0.56, "Идеологи"),
    "by_minsk_obl": _r("Минская область", "oblast", "by_ssr", 0.08, 0.09, 0.50, "Реформаторы"),
    "by_gomel_obl": _r("Гомельская область", "oblast", "by_ssr", 0.05, 0.12, 0.40, "Регионы"),
    "by_brest_obl": _r("Брестская область", "oblast", "by_ssr", 0.04, 0.10, 0.36, "Регионы"),
    # --- Казахская ССР ---
    "kk_ssr": _r("Казахская ССР", "republic", "union", 0.08, 0.15, 0.64, "Регионы"),
    "kk_alma_obl": _r("Алма-Атинская область", "oblast", "kk_ssr", 0.06, 0.09, 0.48, "Регионы"),
    "kk_karaganda_obl": _r("Карагандинская область", "oblast", "kk_ssr", 0.09, 0.06, 0.52, "ВПК"),
    "kk_chimkent_obl": _r("Чимкентская область", "oblast", "kk_ssr", 0.05, 0.11, 0.40, "Регионы"),
    # --- Узбекская ССР ---
    "uz_ssr": _r("Узбекская ССР", "republic", "union", 0.05, 0.14, 0.52, "Регионы"),
    "uz_tashkent_obl": _r("Ташкентская область", "oblast", "uz_ssr", 0.06, 0.10, 0.48, "Регионы"),
    "uz_samarkand_obl": _r("Самаркандская область", "oblast", "uz_ssr", 0.04, 0.12, 0.38, "Регионы"),
    "uz_fergana_obl": _r("Ферганская область", "oblast", "uz_ssr", 0.04, 0.11, 0.42, "Регионы"),
    # --- Грузинская ССР ---
    "ge_ssr": _r("Грузинская ССР", "republic", "union", 0.05, 0.08, 0.42, "Реформаторы"),
    "ge_tbilisi_obl": _r("Тбилиси — промзона", "oblast", "ge_ssr", 0.06, 0.05, 0.45, "Реформаторы"),
    "ge_kutaisi_obl": _r("Кутаисская область", "oblast", "ge_ssr", 0.04, 0.07, 0.35, "Регионы"),
    "ge_batumi_raikom": _r("Батумский обком (узел)", "raikom", "ge_ssr", 0.03, 0.04, 0.38, "Регионы"),
    # --- Армянская ССР ---
    "am_ssr": _r("Армянская ССР", "republic", "union", 0.04, 0.06, 0.32, "Идеологи"),
    "am_yerevan_obl": _r("Ереван — область", "oblast", "am_ssr", 0.05, 0.04, 0.40, "Реформаторы"),
    "am_leninakan_obl": _r("Ленинаканский промузел", "oblast", "am_ssr", 0.03, 0.05, 0.30, "Регионы"),
    "am_razdan_raikom": _r("Разданский райком", "raikom", "am_ssr", 0.02, 0.04, 0.26, "Регионы"),
    # --- Азербайджанская ССР ---
    "az_ssr": _r("Азербайджанская ССР", "republic", "union", 0.07, 0.07, 0.38, "Реформаторы"),
    "az_baku_obl": _r("Бакинская агломерация", "oblast", "az_ssr", 0.09, 0.04, 0.48, "ВПК"),
    "az_sumgait_obl": _r("Сумгаит — химия", "oblast", "az_ssr", 0.06, 0.02, 0.40, "ВПК"),
    "az_ganja_raikom": _r("Кировабадский узел", "raikom", "az_ssr", 0.03, 0.05, 0.32, "Регионы"),
    # --- Прибалтика ---
    "lt_ssr": _r("Литовская ССР", "republic", "union", 0.04, 0.06, 0.32, "Реформаторы"),
    "lt_vilnius_obl": _r("Вильнюсская область", "oblast", "lt_ssr", 0.05, 0.05, 0.36, "Реформаторы"),
    "lt_kaunas_obl": _r("Каунасская область", "oblast", "lt_ssr", 0.04, 0.07, 0.30, "Регионы"),
    "lv_ssr": _r("Латвийская ССР", "republic", "union", 0.03, 0.05, 0.28, "Идеологи"),
    "lv_riga_obl": _r("Рижская область", "oblast", "lv_ssr", 0.04, 0.04, 0.34, "Реформаторы"),
    "lv_daugavpils_obl": _r("Даугавпилсский промузел", "oblast", "lv_ssr", 0.03, 0.05, 0.26, "Регионы"),
    "ee_ssr": _r("Эстонская ССР", "republic", "union", 0.03, 0.04, 0.28, "Реформаторы"),
    "ee_tallinn_obl": _r("Таллин — область", "oblast", "ee_ssr", 0.04, 0.04, 0.32, "Реформаторы"),
    "ee_narva_obl": _r("Нарвский промышленный район", "oblast", "ee_ssr", 0.03, 0.03, 0.28, "ВПК"),
    # --- Молдавия, Средняя Азия ---
    "md_ssr": _r("Молдавская ССР", "republic", "union", 0.03, 0.10, 0.22, "Регионы"),
    "md_kishinev_obl": _r("Кишинёвская область", "oblast", "md_ssr", 0.03, 0.11, 0.28, "Регионы"),
    "md_tiraspol_raikom": _r("Тираспольский узел", "raikom", "md_ssr", 0.02, 0.06, 0.24, "Регионы"),
    "tj_ssr": _r("Таджикская ССР", "republic", "union", 0.02, 0.09, 0.18, "Регионы"),
    "tj_leninabad_obl": _r("Ленинабадская область", "oblast", "tj_ssr", 0.02, 0.10, 0.20, "Регионы"),
    "tj_kurgan_obl": _r("Курган-Тюбинская зона", "oblast", "tj_ssr", 0.02, 0.08, 0.16, "Регионы"),
    "kg_ssr": _r("Кыргызская ССР", "republic", "union", 0.02, 0.07, 0.16, "Регионы"),
    "kg_osh_obl": _r("Ошская область", "oblast", "kg_ssr", 0.02, 0.08, 0.18, "Регионы"),
    "kg_frunze_obl": _r("Фрунзенская область", "oblast", "kg_ssr", 0.02, 0.06, 0.18, "Регионы"),
}


def assignable_region_ids():
    """Регионы, куда можно назначить игрока на старте (область / обком / райком)."""
    return [k for k, v in REGION_META.items() if v.get("type") in ("oblast", "raikom")]


def republic_ids():
    return [k for k, v in REGION_META.items() if v.get("type") == "republic"]


def children_of_republic(rep_id: str):
    return [k for k, v in REGION_META.items() if v.get("parent_republic") == rep_id]
