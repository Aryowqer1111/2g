# 🔹 НОВОЕ: секретариат обкома — 4 заместителя, «совещание» (событие раз в месяц симуляции)
import random
from typing import Any, Dict, List, Optional

SECRETARIAT_ROLES = [
    ("second_secretary", "2-й секретарь обкома"),
    ("ideology", "Секретарь (идеология)"),
    ("industry", "Секретарь (промышленность)"),
    ("agriculture", "Секретарь (сельское хозяйство)"),
]

AGENDAS = ("консерватор", "реформатор", "карьерист")

# 🔹 НОВОЕ: сценарии заседания — выбор игрока → список эффектов (как pending-записи)
SECRETARIAT_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "dir_conflict": {
        "title": "Конфликт директоров",
        "body": "Два директора комбинатов требуют перераспределения фонда; аппарат расколот.",
        "options": {
            "mediate": [
                {"target": "obkom_bureau_tension", "delta": -5.0, "source": "secretariat"},
                {"target": "stability", "delta": 1.5, "source": "secretariat"},
            ],
            "purge": [
                {"target": "obkom_bureau_tension", "delta": 8.0, "source": "secretariat"},
                {"type": "career_score_delta", "delta": 3.0, "source": "purge", "log": "🔹 Жёсткая линия: кадры зачищены"},
                {"target": "corruption_risk", "delta": 0.4, "source": "secretariat"},
            ],
            "escalate_cc": [
                {"target": "plan_pressure", "delta": 0.08, "source": "secretariat"},
                {"target": "kgb_attention", "delta": 1.2, "source": "secretariat"},
            ],
        },
    },
    "moscow_query": {
        "title": "Запрос из Москвы",
        "body": "ЦК требует пояснений по выполнению плана; нужна позиция секретариата.",
        "options": {
            "optimistic_report": [
                {"target": "corruption_risk", "delta": 0.35, "source": "moscow_query"},
                {"type": "career_score_delta", "delta": 5.0, "source": "report", "log": "📞 Оптимистичный отчёт в ЦК"},
            ],
            "honest_report": [
                {"target": "stability", "delta": -1.0, "source": "moscow_query"},
                {"target": "clan_affinity", "delta": 4.0, "source": "moscow_query"},
            ],
            "delay": [
                {"target": "obkom_bureau_tension", "delta": 6.0, "source": "moscow_query"},
                {"target": "political_capital", "delta": -3.0, "source": "moscow_query"},
            ],
        },
    },
    "leak": {
        "title": "Утечка информации",
        "body": "Слухи о «теневом» распределении фондов; пресса и КГБ настороже.",
        "options": {
            "find_scapegoat": [
                {"target": "corruption_risk", "delta": 0.5, "source": "leak"},
                {"type": "career_faction_support_delta", "delta": -5.0, "source": "leak"},
                {"target": "prestige", "delta": -2.0, "source": "leak"},
            ],
            "circle_wagons": [
                {"target": "kgb_attention", "delta": 2.0, "source": "leak"},
                {"target": "obkom_bureau_tension", "delta": -3.0, "source": "leak"},
            ],
            "open_inquiry": [
                {"target": "stability", "delta": 2.0, "source": "leak"},
                {"target": "corruption_risk", "delta": -0.25, "source": "leak"},
                {"target": "political_capital", "delta": -4.0, "source": "leak"},
            ],
        },
    },
}


def _rand_deputy(slot: str, title: str) -> Dict[str, Any]:
    return {
        "slot": slot,
        "title": title,
        "loyalty": round(random.uniform(42.0, 92.0), 1),
        "competence": round(random.uniform(38.0, 88.0), 1),
        "clan_tie": round(random.uniform(20.0, 85.0), 1),
        "hidden_agenda": random.choice(AGENDAS),
    }


def ensure_obkom_secretariat(state: Dict[str, Any]) -> None:
    if state.get("obkom_secretariat"):
        return
    state["obkom_secretariat"] = [_rand_deputy(s, t) for s, t in SECRETARIAT_ROLES]


def secretariat_avg_loyalty(state: Dict[str, Any]) -> float:
    deps: List[Dict[str, Any]] = state.get("obkom_secretariat") or []
    if not deps:
        return 55.0
    return sum(float(d.get("loyalty", 55.0)) for d in deps) / len(deps)


def secretariat_avg_competence(state: Dict[str, Any]) -> float:
    deps = state.get("obkom_secretariat") or []
    if not deps:
        return 55.0
    return sum(float(d.get("competence", 55.0)) for d in deps) / len(deps)


def maybe_roll_secretariat_dilemma(state: Dict[str, Any]) -> None:
    if state.get("secretariat_dilemma"):
        return
    if random.random() > 0.36:
        return
    key = random.choice(list(SECRETARIAT_SCENARIOS.keys()))
    scen = SECRETARIAT_SCENARIOS[key]
    state["secretariat_dilemma"] = {
        "key": key,
        "title": scen["title"],
        "body": scen["body"],
        "options": list(scen["options"].keys()),
    }
    logs = state.get("logs")
    if logs is not None:
        logs.insert(0, f"📋 Совещание аппарата: {scen['title']}")


def expand_secretariat_choice(key: str, choice: str) -> List[Dict[str, Any]]:
    scen = SECRETARIAT_SCENARIOS.get(key) or {}
    opts = scen.get("options") or {}
    return list(opts.get(choice, []))


def clear_secretariat_dilemma(state: Dict[str, Any]) -> None:
    state["secretariat_dilemma"] = None
