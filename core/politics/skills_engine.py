import random
from data.skills_config import FACTION_SKILL_BIASES, COMMITTEE_SKILL_REQUIREMENTS, COMMITTEE_BONUS_MAP

class SkillsEngine:
    def __init__(self):
        self.competencies = {}

    def generate_competencies(self, df):
        competencies_map = {}
        for _, row in df.iterrows():
            mid = row["ID"]
            fac = row["Фракция"]
            biases = FACTION_SKILL_BIASES.get(fac, FACTION_SKILL_BIASES["Регионы"])
            skills = {}
            for skill in ["Военное дело", "Интриги", "Дипломатия", "Хозяйственность"]:
                base = random.gauss(4.5, 1.8)
                val = max(1.0, min(10.0, base + biases[skill]))
                if random.random() < 0.06:
                    val = random.uniform(7.1, 9.8)
                skills[skill] = round(val, 1)
            competencies_map[mid] = skills
        self.competencies.update(competencies_map)
        return self.competencies

    def calculate_committee_bonus(self, member_id, committee_name):
        if member_id not in self.competencies:
            return 0.0
        comp = self.competencies[member_id]
        reqs = COMMITTEE_SKILL_REQUIREMENTS.get(committee_name, {})
        if not reqs:
            return 0.0

        score = sum(comp[s] * w for s, w in reqs.items())
        weight_sum = sum(reqs.values())
        avg_skill = score / weight_sum

        match_factor = max(0, min(1.0, (avg_skill - 4.0) / 4.0))

        if avg_skill >= 8.0:
            base_bonus = 0.5
        elif avg_skill >= 6.5:
            base_bonus = 0.3
        elif avg_skill >= 5.0:
            base_bonus = 0.15
        else:
            base_bonus = 0.05

        return base_bonus * match_factor

    def apply_monthly_effects(self, state):
        effects_keys = ["stability", "budget", "support", "ideology", "prestige", "security"]
        weighted_effects = {k: 0.0 for k in effects_keys}

        comm_eng = state.committee_engine

        for mid, commits in comm_eng.members_assignments.items():
            for comm_name in commits:
                bonus = self.calculate_committee_bonus(str(mid), comm_name)
                if bonus > 0:
                    target_stats = COMMITTEE_BONUS_MAP.get(comm_name, {})
                    for stat, weight in target_stats.items():
                        if stat in weighted_effects:
                            weighted_effects[stat] += bonus * weight

        for stat, value in weighted_effects.items():
            if abs(value) > 0.05:
                current = state.get(stat, 0.0)
                # 🔹 БЕЗ *0.25 — полный месячный эффект
                if stat == "budget":
                    state[stat] = max(-50, min(150, current + value))
                elif stat in ["stability", "support", "ideology", "prestige", "security"]:
                    state[stat] = max(0, min(100, current + value))

        changes = {k: v for k, v in weighted_effects.items() if v > 0.05}
        if changes:
            parts = [f"{k.capitalize()}:{v:+.2f}" for k, v in changes.items()]
            state.logs.insert(0, "⚙️ Комиссии: " + ", ".join(parts))