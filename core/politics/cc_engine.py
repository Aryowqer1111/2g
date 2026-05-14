import pandas as pd
import random
from data.names_db import generate_soviet_name

class CCEngine:
    def __init__(self):
        self.target_size = 150

    def monthly_step(self, state):
        # 🔹 ИСПРАВЛЕНО: доступ через квадратные скобки
        df = state["cc_members"].copy()
        deaths = []

        # 1. Расчет смертей
        for index, row in df.iterrows():
            age = row["Возраст"]
            health = row["Здоровье"]

            base_risk = 0.0005  # Месячный риск
            age_factor = ((age - 40) / 10) ** 2 if age > 40 else 0
            health_factor = max(0.1, 1 - (health / 100))

            monthly_death_chance = base_risk * (1 + age_factor) * (1 + health_factor)

            if random.random() < monthly_death_chance:
                deaths.append(index)

        # 2. Обработка умерших
        if deaths:
            dead_names = df.loc[deaths, "ФИО"].tolist()
            df.drop(deaths, inplace=True)
            df.reset_index(drop=True, inplace=True)
            state["logs"].insert(0, f"⚰️ Ушли из жизни: {', '.join(dead_names[:3])}...")

            alive_ids = set(df["ID"].astype(str).values)
            cleaned_assignments = {}
            # 🔹 ИСПРАВЛЕНО: доступ к committee_engine через st.session_state
            comm_eng = __import__('streamlit').session_state.get("committee_engine")
            if comm_eng:
                for mid, commits in comm_eng.members_assignments.items():
                    if str(mid) in alive_ids:
                        cleaned_assignments[mid] = commits
                comm_eng.members_assignments = cleaned_assignments

        # 3. Дозабор до 150
        current_count = len(df)
        if current_count < self.target_size:
            needed = self.target_size - current_count
            new_members = []
            for _ in range(needed):
                full_name, ethnicity = generate_soviet_name()
                new_members.append({
                    "ID": f"CC_{random.randint(1000, 9999)}", "ФИО": full_name, "Этнос": ethnicity,
                    "Возраст": random.randint(35, 55), "Здоровье": round(random.uniform(80, 100), 1),
                    "Идеология": round(random.uniform(-50, 50), 1),
                    "Лояльность Генсеку": round(random.uniform(50, 90), 1),
                    "Амбиции": round(random.uniform(40, 80), 1),
                    "Вес региона": round(random.uniform(20, 80), 1),
                    "Фракция": random.choice(["Идеологи", "Реформаторы", "ВПК", "Регионы"])
                })

            new_df = pd.DataFrame(new_members)
            df = pd.concat([df, new_df], ignore_index=True)
            if needed > 0:
                state["logs"].insert(0, f"🆕 Кооптировано {needed} новых членов ЦК.")
                # 🔹 ИСПРАВЛЕНО: доступ к skills_engine через st.session_state
                skills_eng = __import__('streamlit').session_state.get("skills_engine")
                if skills_eng:
                    skills_eng.generate_competencies(new_df)

        # 4. Итоговое обновление
        # 🔹 ИСПРАВЛЕНО: сохранение через квадратные скобки
        state["cc_members"] = df

        # 🔹 ИСПРАВЛЕНО: доступ к skills_engine через st.session_state
        skills_eng = __import__('streamlit').session_state.get("skills_engine")
        comm_eng = __import__('streamlit').session_state.get("committee_engine")
        if skills_eng and comm_eng:
            # Передаём state, так как apply_monthly_effects может ожидать его
            skills_eng.apply_monthly_effects(state)

        # 5. 🔹 ОБНОВЛЕНИЕ КАРЬЕРЫ ИГРОКА (гарантированно)
        # 🔹 ИСПРАВЛЕНО: доступ к career и player_cc_id через st.session_state
        career = __import__('streamlit').session_state.get("career")
        player_id = __import__('streamlit').session_state.get("player_cc_id")

        if career and player_id:
            blk = int(state.get("career_growth_block_turns", 0))
            if blk > 0:
                state["career_growth_block_turns"] = blk - 1
                state["logs"].insert(0, "⏸ Блок карьерного роста (пленум / «варяг»): месяц без прироста очков.")
            else:
                player_row = df[df["ID"] == player_id]
                if not player_row.empty:
                    progress = career.calc_progress(state)
                    career.score += progress
                    if career.advance_check(state):
                        from core.politics.career import CAREER_TIERS
                        tier_name = CAREER_TIERS[career.level_idx].name
                        state["logs"].insert(0, f"🎖️ Карьера! Новый уровень: {tier_name}")
                else:
                    progress = career.calc_progress(state)
                    career.score += progress
                    if career.advance_check(state):
                        from core.politics.career import CAREER_TIERS
                        tier_name = CAREER_TIERS[career.level_idx].name
                        state["logs"].insert(0, f"🎖️ Карьера! Новый уровень: {tier_name}")