import random
from typing import Any, Dict, List

import streamlit as st

from core.politics.obkom_secretariat import (
    clear_secretariat_dilemma,
    ensure_obkom_secretariat,
    expand_secretariat_choice,
    maybe_roll_secretariat_dilemma,
)
from core.politics.regional_voting import (
    maybe_spawn_petition,
    resolve_regional_plenum_vote,
    tick_regional_plenum_timer,
)
from data.historical_config import HISTORICAL_PHASES, get_era_modifiers, sync_historical_phase_from_year


def _repair_state_refs_from_session(state: Dict[str, Any]) -> None:
    if state.get("career") is None and st.session_state.get("career") is not None:
        state["career"] = st.session_state["career"]
    if state.get("player_profile") is None and st.session_state.get("player_profile") is not None:
        state["player_profile"] = st.session_state["player_profile"]


def _maybe_seat_hero_in_apparatus(state: Dict[str, Any]) -> None:
    if state.get("obkom_hero_seated"):
        return
    if float(state.get("obkom_hero_ascent", 0.0)) < 100.0:
        return
    hero_id = state.get("obkom_hero_cc_id")
    apparatus = state.get("obkom_apparatus")
    if not hero_id or not isinstance(apparatus, list):
        return
    cc_df = state.get("cc_members")
    if cc_df is None or cc_df.empty:
        return
    hit = cc_df[cc_df["ID"].astype(str) == str(hero_id)]
    if hit.empty:
        return
    name = str(hit.iloc[0]["ФИО"])
    row = {
        "role": "Куратор ЦК на обкоме (выдвижение)",
        "cc_id": str(hero_id),
        "name": name,
        "faction": str(hit.iloc[0]["Фракция"]),
        "is_cc_member": True,
    }
    apparatus.insert(0, row)
    state["obkom_apparatus"] = apparatus
    state["obkom_hero_seated"] = True
    logs = state.get("logs")
    if logs is not None:
        logs.insert(0, f"🎖 Герой ЦК {name} получает пост в аппарате обкома.")


def _flatten_secretariat_choices(queue: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for eff in queue:
        if eff.get("type") == "secretariat_choice":
            key = eff.get("scenario_key")
            choice = eff.get("choice")
            out.extend(expand_secretariat_choice(str(key), str(choice)))
        else:
            out.append(eff)
    return out


class GameLoop:
    def __init__(self):
        self.execution_order = ["politics", "economy", "foreign", "social", "events"]

    def tick(self, state: Dict[str, Any]) -> Dict[str, Any]:
        _repair_state_refs_from_session(state)
        state["turn"] += 1
        state["month"] += 1
        if state["month"] > 12:
            state["month"] = 1
            state["year"] += 1
            logs = state.get("logs")
            if logs is not None:
                logs.insert(0, f"📅 {state['month']}.{state['year']} — Новый год.")

        sync_historical_phase_from_year(state)
        ensure_obkom_secretariat(state)

        comm_eng = st.session_state.get("committee_engine")
        if comm_eng and state.get("cc_members") is not None:
            comm_eng.auto_fill_by_system(state)

        cc_eng = st.session_state.get("cc_engine")
        if cc_eng and state.get("cc_members") is not None:
            cc_eng.monthly_step(state)

        tick_regional_plenum_timer(state)
        maybe_roll_secretariat_dilemma(state)
        maybe_spawn_petition(state)
        _maybe_seat_hero_in_apparatus(state)

        self._apply_effects(state)

        era = get_era_modifiers(int(state.get("year", 1960)))
        phase_key = state.get("historical_phase", "thaw")
        cg = HISTORICAL_PHASES.get(phase_key, HISTORICAL_PHASES["thaw"]).get("corruption_growth", 1.0)
        cg *= float(era.get("corruption_mult", 1.0))
        cr = float(state.get("corruption_risk", 0.0)) + 0.015 * float(cg)
        state["corruption_risk"] = max(0.0, min(10.0, cr))

        self._record_metrics(state)
        _repair_state_refs_from_session(state)
        for k, v in state.items():
            st.session_state[k] = v

        return state

    def _apply_effects(self, state: Dict[str, Any]) -> None:
        raw = list(state.get("pending_effects", []))
        if any(e.get("type") == "secretariat_choice" for e in raw):
            clear_secretariat_dilemma(state)
        queue = _flatten_secretariat_choices(raw)

        for eff in queue:
            etype = eff.get("type")
            source = eff.get("source", "system")

            if etype == "regional_plenum_vote":
                resolve_regional_plenum_vote(state, eff)
                continue

            if etype == "petition_resolve":
                pid = str(eff.get("petition_id", ""))
                action = str(eff.get("action", "ignore"))
                q = list(state.get("petitions_queue") or [])
                state["petitions_queue"] = [p for p in q if str(p.get("id")) != pid]
                logs = state.get("logs")
                if action == "ignore":
                    state["stability"] = max(0.0, float(state.get("stability", 70.0)) - 2.5)
                    if logs is not None:
                        logs.insert(0, f"[{source}] Жалоба проигнорирована — рост недовольства.")
                elif action == "fulfill":
                    state["budget"] = max(0.0, float(state.get("budget", 50.0)) - 3.0)
                    state["support"] = min(100.0, float(state.get("support", 65.0)) + 2.0)
                    if logs is not None:
                        logs.insert(0, f"[{source}] Жалоба удовлетворена: бюджет −, поддержка +.")
                elif action == "reject_unfair":
                    state["prestige"] = max(0.0, float(state.get("prestige", 60.0)) - 3.0)
                    state["kgb_attention"] = min(30.0, float(state.get("kgb_attention", 8.0)) + 1.5)
                    if logs is not None:
                        logs.insert(0, f"[{source}] Отказ без мотива — риск «бунта», внимание КГБ.")
                continue

            if etype == "phone_right_minister":
                pcost = float(eff.get("cost", 8.0))
                pc = float(state.get("political_capital", 40.0))
                if pc < pcost:
                    if state.get("logs") is not None:
                        state["logs"].insert(0, "📵 Недостаточно political_capital для звонка.")
                    continue
                state["political_capital"] = max(0.0, pc - pcost)
                state["plan_pressure"] = max(0.5, min(2.5, float(state.get("plan_pressure", 1.0)) + 0.12))
                state["corruption_risk"] = min(10.0, float(state.get("corruption_risk", 0.0)) + 1.0)
                if state.get("career") is not None:
                    state["career"].reputation = min(100.0, state["career"].reputation + 1.5)
                if state.get("logs") is not None:
                    state["logs"].insert(0, f"[{source}] Телефонное право: временный бонус плана, риск коррупции.")
                continue

            if etype == "career_score_delta":
                career = state.get("career")
                if career is not None:
                    career.score = max(0.0, career.score + float(eff.get("delta", 0.0)))
                    msg = eff.get("log") or f"[{source}] Карьера: очки скорректированы."
                    if state.get("logs") is not None:
                        state["logs"].insert(0, msg)
                continue

            if etype == "career_faction_support_delta":
                career = state.get("career")
                if career is not None:
                    career.faction_support = max(
                        0.0, min(100.0, career.faction_support + float(eff.get("delta", 0.0)))
                    )
                    if state.get("logs") is not None:
                        state["logs"].insert(0, f"[{source}] Фракционная поддержка изменена.")
                continue

            if etype == "clan_request_bonus":
                if random.random() < 0.42 and float(state.get("corruption_risk", 0.0)) >= 4.0:
                    if state.get("logs") is not None:
                        state["logs"].insert(
                            0,
                            f"[{source}] Клан смягчил ход проверки — риск снижен (неформальная сеть).",
                        )
                    state["corruption_risk"] = max(0.0, float(state.get("corruption_risk", 0.0)) - 1.2)
                continue

            target = eff.get("target")
            delta = float(eff.get("delta", 0.0))

            if target == "clan_affinity":
                old = float(state.get("clan_affinity", 50.0))
                state["clan_affinity"] = max(0.0, min(100.0, old + delta))
                if abs(state["clan_affinity"] - old) > 0.01 and state.get("logs") is not None:
                    state["logs"].insert(
                        0,
                        f"[{source}] clan_affinity {'+' if delta > 0 else ''}{state['clan_affinity'] - old:.2f}",
                    )
                continue

            if target == "corruption_risk":
                old = float(state.get("corruption_risk", 0.0))
                state["corruption_risk"] = max(0.0, min(10.0, old + delta))
                if abs(state["corruption_risk"] - old) > 0.01 and state.get("logs") is not None:
                    state["logs"].insert(
                        0,
                        f"[{source}] corruption_risk {'+' if delta > 0 else ''}{state['corruption_risk'] - old:.2f}",
                    )
                continue

            if target == "plan_pressure":
                old = float(state.get("plan_pressure", 1.0))
                state["plan_pressure"] = max(0.5, min(2.5, old + delta))
                if abs(state["plan_pressure"] - old) > 0.01 and state.get("logs") is not None:
                    state["logs"].insert(
                        0,
                        f"[{source}] plan_pressure {'+' if delta > 0 else ''}{state['plan_pressure'] - old:.2f}",
                    )
                continue

            if target == "kgb_attention":
                old = float(state.get("kgb_attention", 8.0))
                state["kgb_attention"] = max(0.0, min(30.0, old + delta))
                if abs(state["kgb_attention"] - old) > 0.01 and state.get("logs") is not None:
                    state["logs"].insert(
                        0,
                        f"[{source}] kgb_attention {'+' if delta > 0 else ''}{state['kgb_attention'] - old:.2f}",
                    )
                continue

            if target == "political_capital":
                old = float(state.get("political_capital", 40.0))
                state["political_capital"] = max(0.0, min(100.0, old + delta))
                if abs(state["political_capital"] - old) > 0.01 and state.get("logs") is not None:
                    state["logs"].insert(
                        0,
                        f"[{source}] political_capital {'+' if delta > 0 else ''}{state['political_capital'] - old:.2f}",
                    )
                continue

            if target in state and isinstance(state[target], (int, float)):
                old = float(state[target])
                cap = 100.0 if state[target] <= 100 else float(state[target])
                state[target] = max(0.0, min(cap, float(state[target]) + delta))
                if abs(float(state[target]) - old) > 0.01 and state.get("logs") is not None:
                    state["logs"].insert(
                        0,
                        f"[{source}] {target} {'+' if delta > 0 else ''}{float(state[target]) - old:.2f}",
                    )

        state["pending_effects"] = []

        cr_kgb = float(state.get("corruption_risk", 0.0))
        if cr_kgb >= 7.0:
            career = state.get("career")
            if career is not None:
                career.score *= 0.3
                career.reputation = max(0.0, career.reputation - 22.0)
            if state.get("logs") is not None:
                state["logs"].insert(
                    0,
                    "🚨 Расследование КГБ: карьерные очки урезаны до 30%, репутация подорвана. "
                    "[мини-квест: заглушка]",
                )
            state["corruption_risk"] = max(0.0, cr_kgb - 2.5)

    def _record_metrics(self, state: Dict[str, Any]) -> None:
        snap = {
            "turn": state["turn"],
            "gdp": state.get("gdp_index", 100),
            "stability": state.get("stability", 70),
            "support": state.get("support", 65),
        }
        state.setdefault("ui_metrics_history", []).append(snap)
        if len(state["ui_metrics_history"]) > 100:
            state["ui_metrics_history"].pop(0)
