from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from data.historical_config import get_era_modifiers
from data.regions_db import REGION_META


@dataclass
class RankTier:
    id: str
    name: str
    score_threshold: int
    unlocked_perms: List[str]
    can_lead_commission: bool
    plenum_vote_power: float
    unlocks_regions: List[str] = field(default_factory=list)


CAREER_TIERS = [
    RankTier("raykom", "Райком", 0, ["local_plan_exec", "micro_budget"], False, 0.0, []),
    RankTier(
        "obkom",
        "Обком",
        200,
        ["regional_budget", "cadre_nominate"],
        True,
        0.25,
        ["regional_commissions", "clan_leverage", "kgb_shadow"],
    ),
    RankTier(
        "sec_central",
        "Секретарь ЦК по отрасли",
        600,
        ["sector_policy", "commission_director"],
        True,
        0.6,
        [],
    ),
    RankTier("cc_member", "Член ЦК КПСС", 1200, ["plenum_vote", "faction_bargain"], True, 1.0, []),
    RankTier("politburo", "Член Политбюро", 2500, ["agenda_draft", "minister_approval"], True, 2.0, []),
    RankTier("gen_sec", "Генеральный секретарь", 5000, ["full_command", "succession_auto"], True, 5.0, []),
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

    def calc_progress(self, state: Dict[str, Any]) -> float:
        region_perf = 70.0
        regions = state.get("regions") or {}
        if self.region_assignment and self.region_assignment in regions:
            region_perf = regions[self.region_assignment]["plan_fulfillment"]

        era = get_era_modifiers(int(state.get("year", 1960)))
        mobility = float(era.get("mobility", 1.0))
        clan_mult = float(era.get("clan_mult", 1.0))
        reform_m = float(era.get("reform_mult", 1.0))

        plan_pressure = float(state.get("plan_pressure", 1.0))
        if self.level_idx == 1:
            plan_pressure *= 1.3

        plan_score = max(0.0, (region_perf - 60.0)) * 0.38 * plan_pressure * mobility
        faction_score = max(0.0, self.faction_support) * 0.22 * mobility
        rep_score = max(0.0, self.reputation) * 0.20 * (0.92 + 0.08 * reform_m)
        block_score = max(0.0, self.block_support) * 0.20
        discipline_penalty = self.disciplinary_incidents * 18.0

        if self.incident_decay_months > 0:
            self.incident_decay_months -= 1
            if self.incident_decay_months == 0:
                self.disciplinary_incidents = max(0, self.disciplinary_incidents - 1)

        base = max(0.0, plan_score + faction_score + rep_score + block_score - discipline_penalty)
        if self.level_idx == 1 and float(state.get("clan_affinity", 50.0)) > 70.0:
            base *= 1.1 * clan_mult
        return base

    def advance_check(self, state: Optional[Dict[str, Any]] = None) -> bool:
        if self.level_idx >= len(CAREER_TIERS) - 1:
            return False
        if self.score < CAREER_TIERS[self.level_idx + 1].score_threshold:
            return False
        self.level_idx += 1
        if state is not None and self.level_idx == 1:
            state["obkom_unlocked"] = True
            tier = CAREER_TIERS[self.level_idx]
            unlocks = ", ".join(tier.unlocks_regions) if tier.unlocks_regions else "—"
            logs = state.get("logs")
            if logs is not None:
                logs.insert(
                    0,
                    f"🏛 Обком: разблокированы региональные рычаги ({unlocks}). "
                    f"Двойственность: план/номенклатура ↔ кланы/КГБ.",
                )
        return True

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
