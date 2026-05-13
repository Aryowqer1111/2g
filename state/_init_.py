import streamlit as st
import pandas as pd
import random
from state.schema import get_clean_state
from core.loop import GameLoop
from core.politics.factions import FactionEngine
from core.politics.committees import CommitteeEngine
from core.politics.skills_engine import SkillsEngine
from core.politics.career import CareerSystem
from data.names_db import generate_soviet_name
from data.regions_db import REGION_META

def init_game():
    if "state" not in st.session_state:
        st.session_state.state = get_clean_state()
        st.session_state.loop = GameLoop()
    if "faction_engine" not in st.session_state: st.session_state.faction_engine = FactionEngine()
    if "committee_engine" not in st.session_state: st.session_state.committee_engine = CommitteeEngine()
    if "skills_engine" not in st.session_state: st.session_state.skills_engine = SkillsEngine()
    if "career" not in st.session_state: st.session_state.career = CareerSystem()

    for k, v in st.session_state.state.items():
        if k not in ["career", "faction_engine", "committee_engine", "skills_engine", "loop", "cc_members", "player_profile"]:
            st.session_state[k] = v

def init_cc_data():
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
        st.session_state.state["cc_members"] = df
        st.session_state.cc_members = df
        if "regions" not in st.session_state:
            regs = {rid: {"active": True, "plan_fulfillment": 85.0, "loyalty": 70.0} for rid in REGION_META}
            st.session_state.state["regions"] = regs; st.session_state.regions = regs
        if hasattr(st.session_state, "skills_engine"): st.session_state.skills_engine.generate_competencies(df)
        if hasattr(st.session_state, "faction_engine"):
            st.session_state.faction_engine.assign_leaders(df)
            st.session_state.faction_engine.update_faction_leaders(df)