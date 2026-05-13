import pandas as pd

class FactionEngine:
    def __init__(self):
        self.historical_leaders = {
            "Идеологи": {"name": "М. Суслов"},
            "Реформаторы": {"name": "А. Косыгин"},
            "ВПК": {"name": "Д. Устинов"},
            "Регионы": {"name": "Л. Брежнев"}
        }
        self.faction_leaders = {}  # {"Идеологи": "CC_ID", ...}

    def _get_best_leader_id(self, df, faction):
        """Внутренний метод: возвращает ID самого влиятельного члена фракции"""
        faction_df = df[df["Фракция"] == faction]
        if faction_df.empty:
            return None
        
        # Вес влияния: Амбиции + Лояльность + Модуль Идеологии
        weights = faction_df["Амбиции"] + faction_df["Лояльность Генсеку"] + faction_df["Идеология"].abs()
        best_idx = weights.idxmax()
        return faction_df.loc[best_idx, "ID"]

    def assign_leaders(self, df: pd.DataFrame):
        """Назначает лидеров фракций при старте игры"""
        for faction, info in self.historical_leaders.items():
            hist_row = df[df["ФИО"] == info["name"]]
            if not hist_row.empty:
                self.faction_leaders[faction] = hist_row.iloc[0]["ID"]
            else:
                leader_id = self._get_best_leader_id(df, faction)
                if leader_id:
                    self.faction_leaders[faction] = leader_id

    def update_faction_leaders(self, df: pd.DataFrame):
        """Автоматическая смена лидера при смерти или падении влияния"""
        for faction, current_id in self.faction_leaders.items():
            # 1. Лидер умер?
            if current_id not in df["ID"].values:
                new_id = self._get_best_leader_id(df, faction)
                if new_id:
                    self.faction_leaders[faction] = new_id
                    print(f"👑 [{faction}] Исторический лидер ушёл. Назначен новый.")
                continue

            # 2. Влияние упало ниже порога?
            leader_row = df[df["ID"] == current_id].iloc[0]
            influence = leader_row["Амбиции"] + leader_row["Лояльность Генсеку"]
            
            if influence < 40:
                new_id = self._get_best_leader_id(df, faction)
                if new_id and new_id != current_id:
                    self.faction_leaders[faction] = new_id
                    print(f"👑 [{faction}] Влияние лидера упало. Фракция сменила главу.")