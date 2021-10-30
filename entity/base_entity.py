from hearthstone.entities import Entity
from hearthstone.enums import GameTag


class BaseEntity:
    # INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 TANK = 3 NEUTRAL = 4
    damage_advantage = [[1, 1, 1, 1, 1], [1, 1, 1, 2, 1], [1, 2, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 1, 1]]

    def __init__(self, entity: Entity):
        self.entity_id = 0
        # GAME = 1 MINION = 4 ENCHANTMENT = 6 LETTUCE_ABILITY = 23
        self.type = 0
        self.name = ''
        # 战场PLAY = 1 墓地GRAVEYARD = 4 手牌SETASIDE = 6  技能LETTUCE_ABILITY = 8
        self.zone = 6
        # LETTUCE_CONTROLLER 2:bot  3:my
        self.controller = 2
        self.entity = entity
        self.parse_entity()

    def get_tag(self, tag_name):
        return self.entity.tags.get(tag_name) or 0

    def parse_entity(self):
        if self.entity is None:
            return
        self.entity_id = self.get_tag(GameTag.ENTITY_ID)
        self.type = self.get_tag(GameTag.CARDTYPE)
        self.zone = self.get_tag(GameTag.ZONE)
        self.controller = self.get_tag(GameTag.LETTUCE_CONTROLLER)

    def __str__(self) -> str:
        return self.__dict__.__str__()
