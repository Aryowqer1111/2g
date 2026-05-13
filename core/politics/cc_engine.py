import pandas as pd
import random
from data.names_db import generate_soviet_name
from .factions import FactionEngine
from .skills_engine import SkillsEngine
from .career import CAREER_TIERS  # Импорт констант для корректного логов

class CCEngine:
    def __init__(self):
        self.target_size = 150

    def monthly_step(self, state):
        # Создаем копию DataFrame во избежание предупреждений Pandas
        df = state.cc_members.copy()
        deaths = []
        
        # 🔹 1. Расчет смертей (недельная вероятность)
        for index, row in df.iterrows():
            age = row["Возраст"]
            health = row["Здоровье"]
            
            base_risk = 0.000125  # 0.0005 / 4 (недельный масштаб)
            age_factor = ((age - 40) / 10) ** 2 if age > 40 else 0
            health_factor = max(0.1, 1 - (health / 100))
            
            weekly_death_chance = base_risk * (1 + age_factor) * (1 + health_factor)
            if random.random() < weekly_death_chance:
                deaths.append(index)
        
        # 2. Обработка умерших
        if deaths:
            dead_names = df.loc[deaths, "ФИО"].tolist()
            df.drop(deaths, inplace=True)
            df.reset_index(drop=True, inplace=True)
            state.logs.insert(0, f"⚰️ Ушли из жизни: {', '.join(dead_names[:3])}...")
            
            alive_ids = set(df["ID"].astype(str).values)
            cleaned_assignments = {}
            for mid, commits in state.committee_engine.members_assignments.items():
                if str(mid) in alive_ids:
                    cleaned_assignments[mid] = commits
            state.committee_engine.members_assignments = cleaned_assignments

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
                state.logs.insert(0, f"🆕 Кооптировано {needed} новых членов ЦК.")
                if hasattr(state, 'skills_engine'):
                    state.skills_engine.generate_competencies(new_df)

        # 4. Итоговое обновление данных ЦК
        state.cc_members = df
        
        # Применяем бонусы комиссии к экономике
        if hasattr(state, 'skills_engine') and hasattr(state, 'committee_engine'):
            state.skills_engine.apply_monthly_effects(state)

        career = state.career
        player_member = state.cc_members[state.cc_members["ID"] == state.player_cc_id]
        
        if not player_member.empty:
            progress = career.calc_monthly_progress(state) # Передаем весь state
            career.score += progress
            
            if career.advance_check():
                tier_name = CAREER_TIERS[career.level_idx].name
                state.logs.insert(0, f"🎖️ Карьера! Новый уровень: {tier_name}")
