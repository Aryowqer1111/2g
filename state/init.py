import copy
import random
import pandas as pd
import streamlit as st
from core.loop import GameLoop
from core.politics.cc_engine import CCEngine
from core.politics.committees import CommitteeEngine
from core.politics.factions import FactionEngine
from core.politics.obkom_bureau import ensure_obkom_apparatus
from core.politics.skills_engine import SkillsEngine
from data.names_db import generate_soviet_name
from data.regions_db import REGION_META
from state.schema import DEFAULT_STATE, get_clean_state

def _repair_nested_state_from_session():
    nested = st.session_state.state
    if nested.get("career") is None and st.session_state.get("career") is not None:
        nested["career"] = st.session_state["career"]
    if nested.get("player_profile") is None and st.session_state.get("player_profile") is not None:
        nested["player_profile"] = st.session_state["player_profile"]

def _sync_flat_session_from_state():
    _repair_nested_state_from_session()
    for k, v in st.session_state.state.items():
        st.session_state[k] = v

def init_game():
    if "state" not in st.session_state:
        st.session_state.state = get_clean_state()
        st.session_state.loop = GameLoop()
    if "faction_engine" not in st.session_state:
        st.session_state.faction_engine = FactionEngine()
    if "committee_engine" not in st.session_state:
        st.session_state.committee_engine = CommitteeEngine()
    if "skills_engine" not in st.session_state:
        st.session_state.skills_engine = SkillsEngine()
    if "cc_engine" not in st.session_state:
        st.session_state.cc_engine = CCEngine()

    nested = st.session_state.state
    # 🔹 Список ключей для инициализации (могут отсутствовать в DEFAULT_STATE)
    optional_keys = [
        "political_capital", "kgb_attention", "obkom_secretariat",
        "secretariat_dilemma", "plenum_months_counter", "regional_plenum_open",
        "regional_plenum_init1", "regional_plenum_init2", "regional_plenum_last_result",
        "petitions_queue", "career_growth_block_turns", "obkom_hero_seated",
        "clan_affinity", "corruption_risk", "plan_pressure", "historical_phase",
        "obkom_apparatus", "obkom_hero_cc_id", "obkom_bureau_tension", "obkom_hero_ascent",
    ]
    for _k in optional_keys:
        if _k not in nested:
            # 🔹 ИСПРАВЛЕНО: используем .get() с дефолтом вместо прямого доступа
            nested[_k] = copy.deepcopy(DEFAULT_STATE.get(_k, None))

    _sync_flat_session_from_state()

def init_cc_data():
    nested = st.session_state.state
    if "cc_members" not in st.session_state or st.session_state.cc_members is None:
        factions = ["Идеологи", "Реформаторы", "ВПК", "Регионы"]
        faction_ideology = {"Идеологи": -60, "Реформаторы": 70, "ВПК": 20, "Регионы": 10}
        members = []
        for i in range(150):
            full_name, ethnicity = generate_soviet_name()
            f = random.choice(factions)
            members.append({
                "ID": f"CC_{i:03d}", "ФИО": full_name, "Этнос": ethnicity,
                "Возраст": random.randint(38, 78), "Здоровье": round(random.uniform(40, 100), 1),
                "Идеология": round(faction_ideology[f] + random.uniform(-20, 20), 1),
                "Лояльность Генсеку": round(random.uniform(25, 98), 1),
                "Амбиции": round(random.uniform(10, 95), 1),
                "Вес региона": round(random.uniform(15, 100), 1), "Фракция": f
            })
        df = pd.DataFrame(members)
        nested["cc_members"] = df
        st.session_state.cc_members = df

        if "skills_engine" in st.session_state:
            st.session_state.skills_engine.generate_competencies(df)
        if "faction_engine" in st.session_state:
            st.session_state.faction_engine.assign_leaders(df)
            st.session_state.faction_engine.update_faction_leaders(df)
        if "committee_engine" in st.session_state:
            st.session_state.committee_engine.auto_fill_faction_balanced(nested)

        # 🔹 Инициализация регионов, если их нет
        if nested.get("regions") is None:
            regs = {rid: {"active": True, "plan_fulfillment": 85.0, "loyalty": 70.0} for rid in REGION_META}
            nested["regions"] = regs
            st.session_state.regions = regs

        if st.session_state.get("cc_members") is not None:
            ensure_obkom_apparatus(nested, st.session_state.cc_members)

    _sync_flat_session_from_state()