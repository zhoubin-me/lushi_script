from .base_entity import BaseEntity


class GameEntity(BaseEntity):

    def __init__(self):
        super().__init__()
        self.players = []
        # 1为选择随从 0为战斗
        self.action_step_type = 1
        self.turn = 0  # 回合数
        # 允许移动随从
        self.allow_move_minion = 0
