# 🔹 НОВОЕ: аппарат обкома — ~95% НЕ члены ЦК; герой — из ЦК, в аппарат не входит, пока не «назначен»
import random
from typing import Any, Dict, List, Optional

import pandas as pd

OBKOM_ROLES: List[str] = [
    "1-й секретарь обкома КПСС",
    "2-й секретарь обкома КПСС",
    "Секретарь обкома (идеология)",
    "Секретарь обкома (организационный)",
    "Зав. сельхозотделом обкома",
    "Зав. промышленным отделом",
    "Зав. кадрами обкома",
    "Председатель облисполкома (союзный)",
    "Зам. председателя облисполкома",
    "Начальник отдела КГБ по области",
    "Председатель обкома профсоюза",
    "Руководитель планового отдела",
    "Главный бухгалтер обкома",
    "Зав. отделом пропаганды",
    "Советник по науке и образованию",
    "Координатор межрайонных парткомов",
    "Спец. по связям с МВД",
    "Доверенный завхоз аппарата",
    "Куратор военной комиссии",
    "Секретарь парткома транспорта",
]

SYNTH_NAMES = [
    "А.П. Силин", "В.Г. Кротов", "М.И. Лебедев", "П.С. Орлов", "Н.К. Фролов",
    "Т.Я. Миронов", "И.В. Степанов", "Ю.Д. Волков", "Е.Ф. Соколов", "Д.Л. Новиков",
]


def _pick_hero_cc_id(cc_df: pd.DataFrame, player_cc_id: Optional[str]) -> str:
    df = cc_df.copy()
    df["ID"] = df["ID"].astype(str)
    if player_cc_id:
        df = df[df["ID"] != str(player_cc_id)]
    if df.empty:
        return str(cc_df.iloc[0]["ID"])
    idx = df["Амбиции"].astype(float).idxmax()
    return str(df.loc[idx, "ID"])


def ensure_obkom_apparatus(state: Dict[str, Any], cc_df: Optional[pd.DataFrame]) -> None:
    if state.get("obkom_apparatus"):
        return
    if cc_df is None or len(cc_df) < 12:
        return

    n_total = min(len(OBKOM_ROLES), 20)
    n_cc_slots = max(1, int(round(n_total * 0.05)))

    pool = cc_df.copy()
    pool["ID"] = pool["ID"].astype(str)
    pool_ids = pool["ID"].tolist()

    hero_id = _pick_hero_cc_id(cc_df, state.get("player_cc_id"))
    eligible = [x for x in pool_ids if x != hero_id]
    n_cc_slots = min(len(eligible), n_cc_slots)
    chosen_cc = random.sample(eligible, n_cc_slots) if eligible else []

    apparatus: List[Dict[str, Any]] = []
    synth_i = 0
    for i, role in enumerate(OBKOM_ROLES[:n_total]):
        if i < len(chosen_cc):
            cid = chosen_cc[i]
            row = pool[pool["ID"] == cid].iloc[0]
            apparatus.append({
                "role": role,
                "cc_id": cid,
                "name": str(row["ФИО"]),
                "faction": str(row["Фракция"]),
                "is_cc_member": True,
            })
        else:
            nm = SYNTH_NAMES[synth_i % len(SYNTH_NAMES)]
            synth_i += 1
            apparatus.append({
                "role": role,
                "cc_id": None,
                "name": f"{nm} (аппарат / не ЦК)",
                "faction": "Аппарат",
                "is_cc_member": False,
            })

    state["obkom_hero_cc_id"] = hero_id
    state["obkom_apparatus"] = apparatus
    state["obkom_hero_seated"] = False
    if state.get("obkom_bureau_tension") is None:
        state["obkom_bureau_tension"] = 40.0
    if state.get("obkom_hero_ascent") is None:
        state["obkom_hero_ascent"] = 8.0
    logs = state.get("logs")
    if logs is None:
        state["logs"] = []
        logs = state["logs"]
    logs.insert(
        0,
        "🏬 Аппарат обкома: ~95% постов — НЕ члены ЦК (райкомы/обкомы); «герой» из ЦК в резерве до назначения.",
    )
