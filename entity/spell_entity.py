from hearthstone.entities import Entity
from hearthstone.enums import GameTag

from .base_entity import BaseEntity


class SpellEntity(BaseEntity):

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.card_id = 0
        self.cost = 0  # 技能速度
        self.lettuce_role = 4
        # 法术种类 NONE = 0 ARCANE = 1 FIRE = 2 FROST = 3 NATURE = 4 HOLY = 5 SHADOW = 6 FEL = 7 PHYSICAL_COMBAT = 8
        self.spell_school = 0
        self.lettuce_cooldown_config = 0  # 技能冷却
        self.lettuce_current_cooldown = 0  # 目前冷却
        self.lettuce_ability_owner = 0  # 技能主人 entity_id
        # 强化状态 例子：集束暗影
        self.powered_up = 0
        # 技能伤害
        self.damage = 0
        # 技能范围: -1随机，6全部
        self.range = 0
        self.parse_entity()

    def parse_entity(self):
        if self.entity is None:
            return
        super(SpellEntity, self).parse_entity()
        self.card_id = self.entity.card_id
        self.cost = self.get_tag(GameTag.COST)
        self.lettuce_role = self.get_tag(GameTag.LETTUCE_ROLE)
        self.spell_school = self.get_tag(GameTag.SPELL_SCHOOL)
        self.lettuce_cooldown_config = self.get_tag(GameTag.LETTUCE_COOLDOWN_CONFIG)
        self.lettuce_current_cooldown = self.get_tag(GameTag.LETTUCE_CURRENT_COOLDOWN)
        self.lettuce_ability_owner = self.get_tag(GameTag.LETTUCE_ABILITY_OWNER)
        self.powered_up = self.get_tag(GameTag.POWERED_UP)

    def read_from_config(self):
        # 从字典读取伤害等参数
        pass
