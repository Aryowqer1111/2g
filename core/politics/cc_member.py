from dataclasses import dataclass, field
from typing import Optional, Dict, List
import random

@dataclass
class CCMember:
    id: str
    name: str
    age: int
    health: float  # 0-100
    ideology_score: float  # -100..100
    ambition: float  # 0-100
    loyalty_to_gen_sec: float  # 0-100
    regional_weight: float  # 0-100 (влияние делегации)
    faction_id: str
    reputation: float = 50.0  # Публичная репутация
    intrigue_points: float = 0.0  # Скрытый ресурс для сделок
    voting_history: List[Dict] = field(default_factory=list)
    
    def monthly_update(self, macro_state: Dict, recent_decisions: List[Dict]):
        def monthly_update(self, macro_state: Dict, recent_decisions: List[Dict]):
    # ... (ваш текущий код обновления) ...

    # 🔹 1. Обновление здоровья
    self.health = max(0, min(100, self.health - random.uniform(0.2, 0.8)))
    if self.age > 65: self.health -= random.uniform(0.5, 1.5)

    # 🔹 2. Расчёт вероятности смерти (ежемесячно)
    base_risk = 0.0005  # 0.05% риск смерти в месяц для молодого человека
    age_factor = ((self.age - 40) / 10) ** 2  # Квадратичный рост риска после 40
    health_factor = max(0.1, 1 - (self.health / 100))  # Чем ниже здоровье, тем выше риск
    
    monthly_death_chance = base_risk * (1 + age_factor) * (1 + health_factor)
    
    # 🔹 3. Проверка на смерть
    if random.random() < monthly_death_chance:
        # 🔥 Смерть! Удаляем из ЦК, обновляем фракции
        self.alive = False
        print(f"💀 [ЦК] {self.name} (ID: {self.id}) скончался в возрасте {self.age} лет.")
        # Тут можно вызвать функцию из cc_engine, чтобы удалить из списка
        # и вызвать перераспределение фракций (если нужно)
        return True # Сигнал, что персонаж умер
    return False
        
        # 2. Лояльность зависит от макро-показателей и решений
        macro_impact = (macro_state.get('stability', 50) - 50) * 0.05 + \
                       (macro_state.get('budget', 0) * 0.02)
        self.loyalty_to_gen_sec = max(0, min(100, 
            self.loyalty_to_gen_sec + macro_impact + random.uniform(-2, 2)
        ))
        
        # 3. Идеологический дрейф от решений
        for dec in recent_decisions:
            diff = abs(dec.get('ideology_shift', 0))
            self.ideology_score += random.uniform(-diff * 0.1, diff * 0.1)
            self.ideology_score = max(-100, min(100, self.ideology_score))
            
        # 4. Амбиции растут при кризисах или успехах
        if macro_state.get('stability', 50) < 40:
            self.ambition = min(100, self.ambition + random.uniform(1, 3))
            
    def should_switch_faction(self, current_faction_stance: float, new_faction_stance: float) -> bool:
        """Меняет фракцию, если текущая политика систематически противоречит позиции"""
        alignment_diff = abs(self.ideology_score - current_faction_stance)
        new_alignment_diff = abs(self.ideology_score - new_faction_stance)
        return new_alignment_diff < (alignment_diff - 15) and random.random() < 0.15
        
    def calculate_vote(self, proposal: Dict, is_open: bool, intrigue_mod: float, player_choice_override: Optional[int] = None) -> Dict:
        """Расчет голоса: 1=За, 0=Против, -1=Воздержался"""
        if player_choice_override is not None:
            vote = player_choice_override
        else:
            # База: лояльность + идеология + вес фракции + интриги
            score = (self.loyalty_to_gen_sec * 0.35) + \
                    (self.ideology_score * proposal.get('ideology_weight', 0) * 0.25) + \
                    (self.regional_weight * 0.15) + \
                    intrigue_mod * 0.25 + random.uniform(-10, 10)
            vote = 1 if score > 55 else (-1 if score < 35 else 0)
            
        # Эффект открытого голосования
        if is_open:
            if vote == 1:
                self.loyalty_to_gen_sec = min(100, self.loyalty_to_gen_sec + 2)
                self.reputation += 1
            elif vote == 0:
                self.loyalty_to_gen_sec = max(0, self.loyalty_to_gen_sec - 4)
                self.reputation -= 2
            else:
                self.reputation -= 0.5
                
        self.voting_history.append({'proposal_id': proposal['id'], 'vote': vote, 'open': is_open})
        return {'member_id': self.id, 'vote': vote, 'reputation_change': self.reputation}
