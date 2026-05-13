from typing import Dict, Any
import streamlit as st

class GameLoop:
    def __init__(self): pass

    def tick(self, state: Dict[str, Any]) -> Dict[str, Any]:
        state["turn"] += 1
        state["month"] += 1
        if state["month"] > 12:
            state["month"] = 1
            state["year"] += 1
            state["logs"].insert(0, f"📅 {state['month']}.{state['year']} — Новый год.")

        state["pending_effects"] = []
        comm_eng = st.session_state.get("committee_engine")
        if comm_eng and state.get("cc_members") is not None:
            comm_eng.auto_fill_by_system(state)

        self._apply_effects(state)
        self._record_metrics(state)
        return state

    def _apply_effects(self, state):
        for eff in state.get("pending_effects", []):
            target = eff.get("target")
            delta = eff.get("delta", 0)
            source = eff.get("source", "system")
            if target in state and isinstance(state[target], (int, float)):
                old = state[target]
                state[target] = max(0, min(100 if state[target]<=100 else state[target], state[target]+delta))
                if abs(state[target]-old) > 0.01:
                    state["logs"].insert(0, f"[{source}] {target} {'+' if delta>0 else ''}{state[target]-old:.2f}")

    def _record_metrics(self, state):
        snap = {"turn": state["turn"], "gdp": state.get("gdp_index",100), "stability": state.get("stability",70), "support": state.get("support",65)}
        state.setdefault("ui_metrics_history", []).append(snap)
        if len(state["ui_metrics_history"]) > 100: state["ui_metrics_history"].pop(0)