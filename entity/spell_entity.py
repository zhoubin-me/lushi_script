from .base_entity import BaseEntity


class SpellEntity(BaseEntity):

    def __init__(self):
        super().__init__()
        self.cost = 0  # 技能速度
        self.lettuce_role = 4
        # 法术种类 NONE = 0 ARCANE = 1 FIRE = 2 FROST = 3 NATURE = 4 HOLY = 5 SHADOW = 6 FEL = 7 PHYSICAL_COMBAT = 8
        self.spell_school = 0
        self.lettuce_cooldown_config = 0  # 技能冷却
        self.lettuce_current_cooldown = 0  # 目前冷却
        self.lettuce_ability_owner = 0  # 技能主人 entity_id
        # 强化状态 例子：集束暗影
        self.powered_up = 0
