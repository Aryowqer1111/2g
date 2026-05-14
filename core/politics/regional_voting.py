# 🔹 НОВОЕ: пленум обкома раз в 6 месяцев, формула голоса, последствия
import random
from typing import Any, Dict, Tuple, List

from data.historical_config import get_era_modifiers
from core.politics.obkom_secretariat import secretariat_avg_loyalty


def tick_regional_plenum_timer(state: Dict[str, Any]) -> None:
    if state.get("regional_plenum_open"):
        return
    c = int(state.get("plenum_months_counter", 0)) + 1
    state["plenum_months_counter"] = c
    if c >= 6:
        state["plenum_months_counter"] = 0
        state["regional_plenum_open"] = True
        state["regional_plenum_init1"] = None
        state["regional_plenum_init2"] = None
        logs = state.get("logs")
        if logs is not None:
            logs.insert(0, "🏛 Созыв пленума обкома: вынесите две инициативы (вкладка управления).")


def compute_plenum_vote_strength(state: Dict[str, Any], initiatives: Tuple[str, str]) -> float:
    era = get_era_modifiers(int(state.get("year", 1960)))
    loyalty = secretariat_avg_loyalty(state)
    clan_w = float(state.get("clan_affinity", 50.0))
    competence_region = 65.0
    regions = state.get("regions") or {}
    career = state.get("career")
    if career is not None and getattr(career, "region_assignment", None):
        rid = career.region_assignment
        if rid in regions and isinstance(regions[rid], dict):
            competence_region = float(regions[rid].get("plan_fulfillment", 65.0))

    raw = loyalty * 0.4 + clan_w * 0.3 + competence_region * 0.2 + random.uniform(-0.1, 0.1)
    raw *= float(era.get("voting_mult", 1.0))
    bonus = 0.0
    if any("план" in (i or "").lower() for i in initiatives):
        bonus += 1.5
    if any("директор" in (i or "").lower() for i in initiatives):
        bonus += 1.0
    return raw + bonus


def resolve_regional_plenum_vote(state: Dict[str, Any], eff: Dict[str, Any]) -> None:
    init1 = eff.get("init1") or "Коррекция плана"
    init2 = eff.get("init2") or "Кадровые перестановки"
    initiatives = (str(init1), str(init2))
    score = compute_plenum_vote_strength(state, initiatives)
    threshold = 52.0 + float(state.get("obkom_bureau_tension", 40.0)) * 0.08
    win = score >= threshold
    logs = state.get("logs")
    if win:
        if logs is not None:
            logs.insert(
                0,
                f"✅ Пленум: инициативы проведены (сила {score:.1f} ≥ {threshold:.1f}). {init1}; {init2}.",
            )
        state["regional_plenum_last_result"] = "win"
    else:
        if logs is not None:
            logs.insert(
                0,
                f"❌ Пленум: поражение (сила {score:.1f} < {threshold:.1f}). Давление «варягов» и фракций.",
            )
        state["regional_plenum_last_result"] = "loss"
        career = state.get("career")
        if career is not None:
            career.reputation = max(0.0, career.reputation - 8.0)
        state["career_growth_block_turns"] = int(state.get("career_growth_block_turns", 0)) + 2
        state["prestige"] = max(0.0, float(state.get("prestige", 60.0)) - 4.0)
        state["kgb_attention"] = min(30.0, float(state.get("kgb_attention", 10.0)) + 2.5)
        if random.random() < 0.45:
            if logs is not None:
                logs.insert(0, "🧳 «Варяг» из центра усиливает кураторство — блокируйте карьеру 2 хода.")
    state["regional_plenum_open"] = False
    state["regional_plenum_init1"] = None
    state["regional_plenum_init2"] = None


def maybe_spawn_petition(state: Dict[str, Any]) -> None:
    if random.random() > 0.42:
        return
    q: List[Dict[str, Any]] = list(state.get("petitions_queue") or [])
    pid = f"PET_{int(state.get('turn', 0))}"
    templates = [
        ("Завод «Красный пролетарий»", "Требование снизить нормы; угроза забастовки."),
        ("Колхоз «Рассвет»", "Жалоба на недопоставку запчастей."),
        ("Жилкомбинат", "Очереди и ветхое жильё — просьба о вмешательстве парткома."),
    ]
    name, text = random.choice(templates)
    q.append({"id": pid, "source": name, "text": text})
    state["petitions_queue"] = q[-8:]
    logs = state.get("logs")
    if logs is not None:
        logs.insert(0, f"📨 Жалоба трудящихся: {name}.")

