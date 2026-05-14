# 🔹 НОВОЕ: исторические фазы + эпохальные модификаторы по году (1960–1991)

HISTORICAL_PHASES = {
    "thaw": {"mobility": 1.2, "control": 0.8, "corruption_growth": 0.5},
    "stagnation": {"mobility": 0.7, "control": 1.0, "corruption_growth": 1.3},
    "transition": {"mobility": 0.72, "control": 1.0, "corruption_growth": 1.15},
    "perestroika": {"mobility": 0.5, "control": 0.6, "corruption_growth": 1.8},
}


def get_era_modifiers(year: int) -> dict:
    """Эпоха по календарю: оттепель / застой / переход / перестройка (месячный тик)."""
    if year < 1960:
        year = 1960
    if year > 1991:
        year = 1991
    if 1960 <= year <= 1964:
        return {
            "id": "thaw",
            "mobility": 1.3,
            "corruption_mult": 0.7,
            "voting_mult": 0.8,
            "clan_mult": 1.0,
            "stability_mult": 1.0,
            "reform_mult": 1.2,
            "instability_mult": 0.9,
        }
    if 1965 <= year <= 1982:
        return {
            "id": "stagnation",
            "mobility": 0.6,
            "corruption_mult": 1.0,
            "voting_mult": 1.0,
            "clan_mult": 1.5,
            "stability_mult": 1.2,
            "reform_mult": 0.85,
            "instability_mult": 1.0,
        }
    if 1983 <= year <= 1984:
        return {
            "id": "transition",
            "mobility": 0.72,
            "corruption_mult": 1.1,
            "voting_mult": 1.1,
            "clan_mult": 1.35,
            "stability_mult": 1.05,
            "reform_mult": 1.05,
            "instability_mult": 1.25,
        }
    return {
        "id": "perestroika",
        "mobility": 0.55,
        "corruption_mult": 1.25,
        "voting_mult": 1.3,
        "clan_mult": 1.2,
        "stability_mult": 0.95,
        "reform_mult": 1.4,
        "instability_mult": 1.8,
    }


def sync_historical_phase_from_year(state: dict) -> None:
    state["historical_phase"] = get_era_modifiers(int(state.get("year", 1960)))["id"]
