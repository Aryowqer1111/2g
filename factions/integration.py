from typing import Dict, List
from core.state import GameState
from core.event_bus import EventBus
from .ai_engine import FactionAI

class FactionManager:
    def __init__(self, bus: EventBus):
        self.ai = FactionAI()
        self.bus = bus
        self._setup_hooks()

    def _setup_hooks(self):
        self.bus.subscribe("month_start", self._on_month_start)
        self.bus.subscribe("player_decision", self._on_decision)

    def _on_month_start(self, state: GameState):
        if not state: return
        logs = self.ai.monthly_simulate(state)
        for log in logs:
            print(f"  🗣 {log}")
            state.log_event(f"Фракции: {log}")

    def _on_decision(self, data: Dict):
        # Реакция на решения игрока (влияет на лояльность)
        if not data: return
        choice = data.get("choice", 0)
        for f in self.ai.factions.values():
            drift = 0.0
            if choice in [1, 4] and f.name in ["Идеологи", "ВПК"]: drift += 2.0
            elif choice in [2, 5] and f.name in ["Реформаторы", "Регионы"]: drift += 2.0
            f.loyalty += drift
        # Проверка доминирующей фигуры
        leader, faction = self.ai.get_dominant_figure()
        print(f"👑 Текущий расклад: лидером может стать {leader} от фракции '{faction}'")

    def show_status(self):
        print("\n📋 ПОЛИТБЮРО И ФРАКЦИИ:")
        print(f"{'Фракция':<12} | {'Лидер':<18} | {'Влияние':<7} | {'Лояльность':<10} | {'Советник':<20} | {'Статус'}")
        print("-" * 90)
        for name, f in self.ai.factions.items():
            adv = f.advisor.name if f.advisor else "Нет"
            trait = "🤝" if f.loyalty > 60 else ("⚠️" if f.loyalty > 30 else "🚨")
            print(f"{name:<12} | {f.leader:<18} | {f.influence:<7.1f} | {f.loyalty:<10.1f} | {adv:<20} | {trait}")

    def handle_vote(self, topic: str = "План пятилетки"):
        passed, summary, pct = self.ai.check_politburo_vote(topic, player_weight=10.0)
        status = "✅ ПРИНЯТО" if passed else "❌ ОТКЛОНЕНО"
        print(f"\n🏛️ Голосование: {topic}")
        print(f"  Результат: {status} ({summary})")
        return passed

    def command_remove(self, name: str):
        success, old, new = self.ai.liquidate_leader(name)
        if success:
            print(f"⚖️ Лидер {old} отстранён. Новый: {new}. Лояльность фракции резко упала.")
        else:
            print("❌ Фракция не найдена.")

    def command_advisor(self, name: str, new_name: str):
        if name in self.ai.factions and self.ai.factions[name].advisor:
            self.ai.factions[name].advisor.name = new_name
            self.ai.factions[name].advisor.loyalty = 70.0
            self.ai.factions[name].advisor.is_betraying = False
            print(f"✅ Советник заменён на {new_name} во фракции '{name}'.")
        else:
            print("❌ Ошибка: фракция не имеет слота советника или не найдена.")