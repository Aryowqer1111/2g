import random

import pandas as pd
import streamlit as st

from core.politics.career import CareerSystem
from data.names_db import generate_soviet_name
from data.regions_db import REGION_META, assignable_region_ids
from state.init import _sync_flat_session_from_state

def render_character_creation():
    st.title("☭ Создание Аппаратчика")
    st.subheader("Определите свою карьеру в системе номенклатуры")
    
    with st.form("char_creation"):
        col1, col2 = st.columns(2)
        last_name = col1.text_input("Фамилия", placeholder="Иванов")
        first_name = col2.text_input("Имя", placeholder="Иван")
        patronymic = st.text_input("Отчество", placeholder="Иванович")

        ethnicity_map = {
            "russian": "Русский", "ukrainian": "Украинец", "belarusian": "Белорус",
            "tatar": "Татарин", "georgian": "Грузин", "armenian": "Армянин",
            "jewish": "Еврей", "uzbek": "Узбек", "azeri": "Азербайджанец",
            "baltic": "Прибалт", "moldovan": "Молдаванин"
        }
        ethnicity_key = st.selectbox("Национальность", list(ethnicity_map.keys()), format_func=ethnicity_map.get)
        age = st.number_input("Возраст", min_value=25, max_value=65, value=35)
        starting_faction = st.selectbox("Политический вектор (Фракция-куратор)", ["Идеологи", "Реформаторы", "ВПК", "Регионы"])
        starting_region = st.selectbox(
            "Начальное назначение (Регион/Обком/Райком)",
            options=assignable_region_ids(),
            format_func=lambda x: REGION_META[x]["name"],
        )

        submitted = st.form_submit_button("✅ Вступить в Партию и начать карьеру")

    if submitted:
        if not last_name or not first_name:
            st.error("Фамилия и Имя обязательны для заполнения.")
            return

        full_name = f"{last_name} {first_name} {patronymic}"
        player_id = f"PLAYER_{random.randint(100, 999)}"

        career = CareerSystem()
        career.faction_support = 65.0
        career.block_support = 75.0
        career.assign_region(starting_region)

        profile = {
            "name": full_name,
            "ethnicity": ethnicity_key,
            "age": age,
            "faction": starting_faction,
            "id": player_id,
        }
        st.session_state.player_profile = profile
        st.session_state.career = career
        st.session_state.player_cc_id = player_id

        st.session_state.state["player_profile"] = profile
        st.session_state.state["career"] = career
        st.session_state.state["player_cc_id"] = player_id
        st.session_state.state["character_created"] = True

        new_row = pd.DataFrame([{
            "ID": player_id, "ФИО": full_name, "Этнос": ethnicity_map[ethnicity_key],
            "Возраст": age, "Здоровье": 95.0, "Идеология": 0.0,
            "Лояльность Генсеку": 75.0, "Амбиции": 80.0,
            "Вес региона": REGION_META[starting_region]["pol_influence"]*100,
            "Фракция": starting_faction
        }])

        if "cc_members" in st.session_state:
            st.session_state.cc_members = pd.concat([st.session_state.cc_members, new_row], ignore_index=True)
        else:
            st.session_state.cc_members = new_row
            
        if "state" in st.session_state:
            st.session_state.state["cc_members"] = st.session_state.cc_members

        _sync_flat_session_from_state()

        st.success(
            f"🎉 Добро пожаловать, товарищ {last_name}! Карьера в {REGION_META[starting_region]['name']} начинается."
        )
        st.rerun()