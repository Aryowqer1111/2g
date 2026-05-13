from dataclasses import dataclass
from typing import List, Optional
from data.regions_db import REGION_META

@dataclass
class RankTier:
    id: str
    name: str
    score_threshold: int
    unlocked_perms: List[str]
    can_lead_commission: bool
    plenum_vote_power: float

CAREER_TIERS = [
    RankTier("raykom", "Райком", 0, ["local_plan_exec", "micro_budget"], False, 0.0),
    RankTier("obkom", "Обком", 200, ["regional_budget", "cadre_nominate"], True, 0.25),
    RankTier("sec_central", "Секретарь ЦК по отрасли", 600, ["sector_policy", "commission_director"], True, 0.6),
    RankTier("cc_member", "Член ЦК КПСС", 1200, ["plenum_vote", "faction_bargain"], True, 1.0),
    RankTier("politburo", "Член Политбюро", 2500, ["agenda_draft", "minister_approval"], True, 2.0),
    RankTier("gen_sec", "Генеральный секретарь", 5000, ["full_command", "succession_auto"], True, 5.0)
]

class CareerSystem:
    def __init__(self):
        self.level_idx = 0
        self.score = 0.0
        self.reputation = 65.0
        self.disciplinary_incidents = 0
        self.incident_decay_months = 0
        self.faction_support = 60.0
        self.block_support = 60.0
        self.region_assignment: Optional[str] = None

    def calc_progress(self, state) -> float:
        region_perf = 70.0
        if self.region_assignment and self.region_assignment in state.get("regions", {}):
            region_perf = state["regions"][self.region_assignment]["plan_fulfillment"]
            
        plan_score = max(0, (region_perf - 60)) * 0.35
        faction_score = max(0, self.faction_support) * 0.25
        rep_score = max(0, self.reputation) * 0.20
        block_score = max(0, self.block_support) * 0.20
        
        discipline_penalty = self.disciplinary_incidents * 18.0
        if self.incident_decay_months > 0:
            self.incident_decay_months -= 1
            if self.incident_decay_months == 0:
                self.disciplinary_incidents = max(0, self.disciplinary_incidents - 1)
        # 🔹 БЕЗ *0.25 — полный месячный прогресс
        return max(0.0, plan_score + faction_score + rep_score + block_score - discipline_penalty)

    def advance_check(self) -> bool:
        if self.level_idx >= len(CAREER_TIERS) - 1:
            return False
        if self.score >= CAREER_TIERS[self.level_idx + 1].score_threshold:
            self.level_idx += 1
            return True
        return False

    def add_incident(self, severity: int = 1):
        self.disciplinary_incidents += severity
        self.incident_decay_months = 6 * severity
        self.reputation = max(0, self.reputation - severity * 12)

    def get_permissions(self) -> List[str]:
        return CAREER_TIERS[self.level_idx].unlocked_perms

    def assign_region(self, region_id: str) -> bool:
        if region_id in REGION_META:
            self.region_assignment = region_id
            return True
        return False