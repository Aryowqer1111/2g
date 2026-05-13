# В player_state.py или аналоге
class PlayerCareer:
    RAYKOM = 0
    OBKOM = 1
    CC_SECRETARY = 2
    CC_MEMBER = 3
    POLITBURO = 4
    GENERAL_SECRETARY = 5

    def __init__(self):
        self.level = PlayerCareer.RAYKOM  # Старт
        self.cc_member_id = None  # Привязка к объекту CCMember

    def get_vote_access(self, engine: CCEngine) -> Optional[int]:
        if self.level >= PlayerCareer.CC_MEMBER:
            # Если игрок в ЦК, движок подставит его ID в голосование
            engine.set_player_membership(self.cc_member_id)
            return None  # Голосование происходит внутри calculate_vote через override
        return None  # Наблюдатель