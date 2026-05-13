from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random

@dataclass
class IntrigueEngine:
    active_deals: List[Dict] = field(default_factory=list)  # Временные союзы/торги
    secrets_known: Dict[str, List[str]] = field(default_factory=dict)  # member_id -> [secrets]
    blackmail_leverage: Dict[str, float] = field(default_factory=dict)  # member_id -> force_mod
    
    def generate_intrigue_phase(self, cc_members: Dict, plenum_context: str):
        """Создает фоновые интриги за 1-2 хода до Пленума"""
        self.active_deals.clear()
        members = list(cc_members.values())
        for _ in range(random.randint(2, 5)):
            m1, m2 = random.sample(members, 2)
            deal_type = random.choice(['vote_swap', 'info_leak', 'blackmail', 'faction_bribe'])
            self.active_deals.append({
                'type': deal_type,
                'participants': [m1.id, m2.id],
                'target_proposal': plenum_context,
                'expires_in': random.randint(1, 3),
                'strength': random.uniform(-15, 15)
            })
            
    def get_modifiers_for_member(self, member_id: str) -> float:
        mod = 0.0
        for deal in self.active_deals:
            if member_id in deal['participants']:
                mod += deal['strength'] * 0.3
        mod += self.blackmail_leverage.get(member_id, 0)
        return mod
    
    def resolve_leaks(self) -> List[str]:
        """Утечки компромата снижают репутацию и лояльность"""
        affected = []
        for m_id, leverage in list(self.blackmail_leverage.items()):
            if random.random() < 0.2:
                affected.append(f"🕵️ Утечка компромата на члена ЦК #{m_id}")
                self.blackmail_leverage[m_id] = 0
        return affected