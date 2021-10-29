class BaseEntity:
    # INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 TANK = 3 NEUTRAL = 4
    damage_advantage = [[1, 1, 1, 1, 1], [1, 1, 1, 2, 1], [1, 2, 1, 1, 1], [1, 1, 2, 1, 1]]

    def __init__(self):
        self.card_id = 0
        self.entity_id = 0
        # GAME = 1 MINION = 4 ENCHANTMENT = 6 LETTUCE_ABILITY = 23
        self.type = 0
        self.name = ''
        # 战场PLAY = 1 墓地GRAVEYARD = 4 手牌SETASIDE = 6  技能LETTUCE_ABILITY = 8
        self.zone = 6
        # LETTUCE_CONTROLLER 2:bot  3:my
        self.controller = 2

    def __str__(self) -> str:
        return self.__dict__.__str__()
