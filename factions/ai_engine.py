import random
from typing import Dict, List
from core.state import GameState
from factions.models import FactionMember

class FactionAI:
    def __init__(self):
        self.factions = {}
        self.politburo_members = []

    def init_1960(self):
        from factions.models import get_1960_start
        self.factions = get_1960_start()
        self.politburo_members = []
        for f in self.factions.values():
            self.politburo_members.extend(f.members)

    def monthly_simulate(self, state: GameState):
        # 🔧 FIX: Проверяем, есть ли атрибут faction у объекта voter и cand
        for voter in self.politburo_members:
            for fac in self.factions.values():
                if voter in fac.members:
                    voter.faction = fac.name  # 🔹 Добавляем поле faction к объекту voter
                    break

        # Симуляция смертей/переходов
        for fac in self.factions.values():
            for member in fac.members[:]:
                member.age_up()
                if member.check_mortality():
                    fac.members.remove(member)
                    if member in self.politburo_members:
                        self.politburo_members.remove(member)
                    # 🔹 Симуляция преемственности
                    if member.is_current_leader:
                        self._start_succession_vote(fac.name, member, state)

    def _start_succession_vote(self, fac_name: str, member: FactionMember, state: GameState):
        """Запускает голосование за нового лидера после смерти/ухода текущего"""
        print(f"⚖️ [AI] Смерть лидера {member.name}. Запуск голосования...")
        candidates = [m for m in self.politburo_members if m.internal_influence > 15]
        if len(candidates) < 2: candidates = self.politburo_members[:5]

        scores = {}
        for cand in candidates:
            scores[cand.name] = 0.0
            for voter in self.politburo_members:
                if not hasattr(voter, 'faction') or not hasattr(cand, 'faction'):
                    continue
                # 🔧 FIX: Проверяем, что у объектов есть поле faction
                voter_fac = getattr(voter, 'faction', 'Независимый')
                cand_fac = getattr(cand, 'faction', 'Независимый')
                
                sc = cand.internal_influence / 100.0
                if voter_fac == cand_fac: sc += 0.35
                elif voter_fac in self.factions and cand_fac in self.factions:
                    if cand_fac in self.factions[voter_fac].rivals: sc -= 0.25
                sc += random.uniform(-0.05, 0.05)
                scores[cand.name] += sc

        winner_name = max(scores, key=scores.get) if scores else None
        if winner_name:
            print(f"✅ [AI] Избран новый лидер: {winner_name}")
            # 🔹 В реальной игре: вызвать engine.apply_succession_result(winner_name)
            # Здесь просто обновим объект
            winner = next((m for m in self.politburo_members if m.name == winner_name), None)
            if winner:
                winner.internal_influence = min(100.0, winner.internal_influence + 25.0)

    def get_leader_by_name(self, name: str) -> FactionMember:
        for m in self.politburo_members:
            if m.name == name:
                return m
        return None