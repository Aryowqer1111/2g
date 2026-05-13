import random
from typing import Dict, List, Tuple
from factions.ai_engine import FactionAI
from .profiles import LeaderProfile
from core.state import GameState
from factions.models import FactionMember

class PolitburoVote:
    def __init__(self, factions: FactionAI, leader: LeaderProfile):
        self.factions = factions
        self.leader = leader
        self.concession_count: int = 0
        self.current_leader_member = None

    def set_current_leader(self, member_name: str):
        for m in self.factions.politburo_members:
            if m.name == member_name:
                self.current_leader_member = m
                break

    def _calculate_stance(self, member, faction, effects: Dict[str, float], deterministic: bool = True) -> Tuple[bool, str]:
        if not faction.priorities: return True, "поддерживает линию ЦК"
        score = sum(faction.priorities.get(k, 0.3) * v for k, v in effects.items())
        norm = score / (sum(faction.priorities.values()) * 5.0 or 1)
        prob = max(0.15, min(0.85, 0.5 + norm * 0.3 + self.leader.authority / 1000))
        yes = prob > 0.5 if deterministic else random.random() < prob
        reason = "укрепляет стабильность" if yes and norm > 0.1 else "подрывает основы" if not yes and norm < -0.1 else "нейтральная позиция"
        return yes, reason

    def predict_stances(self, effects: Dict[str, float]) -> List[Dict]:
        stances = []
        for m in self.factions.politburo_members:
            fac = next((f for f in self.factions.factions.values() if m in f.members), None)
            if not fac: continue
            voted_yes, reason = self._calculate_stance(m, fac, effects, True)
            stances.append({"name": m.name, "faction": fac.name, "vote": "✅" if voted_yes else "❌", "reason": reason})
        return stances

    def evaluate_agenda(self, event_effects: Dict[str, float], event_title: str = "") -> Dict:
        members = self.factions.politburo_members if hasattr(self.factions, 'politburo_members') else []
        if not members: return {"passed": False, "approval": 0.0, "details": [], "summary": "📉 Политбюро пусто"}
        details, yes = [], 0
        for m in members:
            fac = next((f for f in self.factions.factions.values() if m in f.members), None)
            if not fac: continue
            voted_yes, reason = self._calculate_stance(m, fac, event_effects, False)
            if voted_yes: yes += 1
            details.append(f"{'✅' if voted_yes else '❌'} {m.name} ({fac.name[:4]}): {reason}")
        approval = (yes / len(members)) * 100.0
        return {"passed": approval >= 55.0, "approval": approval, "details": details, "summary": f"📊 Реакция: {event_title} | {approval:.0f}% {'✅ ОДОБРЕНО' if approval >= 55.0 else '❌ ОТКЛОНЕНО'}"}

    def run_succession_vote(self, candidates: List) -> Tuple[str, Dict]:
        votes = {c.name: 0 for c in candidates}
        details = []
        for voter in self.factions.politburo_members:
            voter_fac = next((f for f in self.factions.factions.values() if voter in f.members), None)
            best = max(candidates, key=lambda c: (0.6 if (voter_fac and next((f for f in self.factions.factions.values() if c in f.members), None) == voter_fac) else 0) + c.internal_influence/100 + (0.5 if c == voter else 0))
            votes[best.name] += 1
            details.append(f"🗳 {voter.name} → {best.name}")
        return max(votes, key=votes.get), {"votes": votes, "summary": f"Голоса: {votes}", "details": details}

    def simulate_succession_vote(self, candidates: List['FactionMember']) -> Dict:
        """Взвешенное голосование Политбюро за нового Генсека"""
        if not candidates: return {"winner": None, "scores": {}, "summary": "❌ Кандидаты отсутствуют", "log": []}
        
        voters = [m for m in self.factions.politburo_members if m not in candidates] # Остальные голосуют
        total_inf = sum(max(1, v.internal_influence) for v in voters) or 1
        scores = {c.name: 0.0 for c in candidates}
        log = []

        for v in voters:
            v_fac = next((f for f in self.factions.factions.values() if v in f.members), None)
            best_c, best_score, reason = None, -1.0, "Компромисс"
            
            for c in candidates:
                c_fac = next((f for f in self.factions.factions.values() if c in f.members), None)
                sc = c.internal_influence / 100.0
                if v_fac and c_fac and v_fac.name == c_fac.name: sc += 0.35
                elif v_fac and c_fac and c_fac.name in v_fac.rivals: sc -= 0.25
                sc += random.uniform(-0.05, 0.05)
                if sc > best_score: best_score, best_c, reason = sc, c, f"Поддержка {c_fac.name if c_fac else 'независимого'}"
                
            if best_c:
                weight = v.internal_influence / total_inf
                scores[best_c.name] += weight * 100
                log.append(f"🗳 {v.name} ({v_fac.name[:4] if v_fac else '?'}) → {best_c.name}")

        winner = max(scores, key=scores.get) if scores else None
        summary = f"📊 Итог: {winner} ({scores[winner]:.1f}%)" if winner else "📊 Никто не набрал большинства"
        return {"winner": winner, "scores": scores, "summary": summary, "log": log}

    def open_vote(self, title: str, state: GameState, use_authority: bool = False) -> Tuple[bool, str, float]:
        return self.run_succession_vote([self.current_leader_member] if self.current_leader_member else [])