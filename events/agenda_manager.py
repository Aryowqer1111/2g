import random
from typing import Dict, Set
from events.templates.economy1 import ECONOMY_AGENDAS
from events.templates.economy2 import DYNAMIC_ECONOMY_AGENDAS

def calculate_economic_health(metrics: Dict) -> float:
    stability = max(0, min(100, metrics.get("stability", 50)))
    budget_normalized = max(0, min(100, metrics.get("budget", 0) + 50))
    avg_eff = max(0, min(100, metrics.get("avg_ministry_efficiency", 50)))
    return round((stability * 0.5) + (budget_normalized * 0.3) + (avg_eff * 0.2), 1)

def get_next_agenda(year: int, used_ids: Set[str], metrics: Dict, 
                    faction_initiatives: list = None, custom_events: list = None) -> Dict:
    health = calculate_economic_health(metrics)
    
    # 🔹 1. Инициативы фракций (ПРИОРИТЕТ: 65% шанс, строго единоразовые)
    if faction_initiatives and random.random() < 0.65:
        available = [i for i in faction_initiatives if i.get("id") not in used_ids]
        if available:
            agenda = random.choice(available)
            used_ids.add(agenda["id"])
            return {"title": f"🗣 Инициатива: {agenda['proposer']}", "text": agenda['description'], 
                    "choices": agenda['choices'], "source": "faction"}
            
    # 🔹 2. Пользовательские события (35% шанс, строго единоразовые, фильтр по году)
    valid_custom = []
    if custom_events:
        for ce in custom_events:
            if getattr(ce, 'id', '') not in used_ids and getattr(ce, 'year', 1960) <= year <= getattr(ce, 'year', 1960) + 2:
                valid_custom.append(ce)
    if valid_custom and random.random() < 0.35:
        ce = random.choice(valid_custom)
        used_ids.add(ce.id)
        return {"title": f"📝 [Пользователь] {ce.title}", "text": ce.description, 
                "choices": ce.choices, "source": "custom"}
                
    # 🔹 3. Динамические события (фильтр по used_ids и condition)
    available_dynamic = [t for t in DYNAMIC_ECONOMY_AGENDAS if t.id not in used_ids]
    if health >= 70: target = "success" if random.random() < 0.60 else ("neutral" if random.random() < 0.85 else "crisis")
    elif health >= 45: target = "success" if random.random() < 0.25 else ("neutral" if random.random() < 0.70 else "crisis")
    else: target = "success" if random.random() < 0.10 else ("neutral" if random.random() < 0.40 else "crisis")
    
    dynamic_pool = [t for t in available_dynamic if t.condition == target]
    
    # 🔹 4. Исторические события (фильтр по used_ids и году)
    unused_historical = [t for t in ECONOMY_AGENDAS if t.id not in used_ids and t.start_year <= year <= t.end_year]
    
    # Логика выбора между динамикой и историей
    if dynamic_pool and (not unused_historical or random.random() < 0.50):
        tmpl = random.choice(dynamic_pool)
        used_ids.add(tmpl.id)
        return {"title": tmpl.title, "text": tmpl.description, "choices": tmpl.choices, "source": "dynamic"}
        
    if unused_historical:
        tmpl = random.choice(unused_historical)
        used_ids.add(tmpl.id)
        return {"title": tmpl.title, "text": tmpl.description, "choices": tmpl.choices, "source": "historical"}
        
    # 🔹 Фолбэк
    return {
        "title": "📋 Плановое заседание Политбюро",
        "text": "Рассмотрение текущих вопросов исполнения директив и корректировки плановых показателей.",
        "choices": [
            {"text": "Утвердить", "effects": {"stability": 1, "budget": 0, "support": 1}},
            {"text": "Отложить", "effects": {"stability": 0, "budget": 0, "support": 0}},
            {"text": "Вернуть на доработку", "effects": {"stability": -1, "budget": 1, "support": -1}}
        ],
        "source": "fallback"
    }