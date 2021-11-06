import random

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
        # 是否是连击技能
        self.combo = 0
        self.lettuce_cooldown_config = 0  # 技能冷却
        self.lettuce_current_cooldown = 0  # 目前冷却
        self.lettuce_ability_owner = 0  # 技能主人 entity_id
        # 强化状态 例子：集束暗影
        self.powered_up = 0
        # 是否是装备
        self.lettuce_is_equpiment = 0
        # 是否是宝藏
        self.lettuce_is_treasure_card = 0
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
        self.combo = self.get_tag(GameTag.COMBO)
        self.lettuce_cooldown_config = self.get_tag(GameTag.LETTUCE_COOLDOWN_CONFIG)
        self.lettuce_current_cooldown = self.get_tag(GameTag.LETTUCE_CURRENT_COOLDOWN)
        self.lettuce_ability_owner = self.get_tag(GameTag.LETTUCE_ABILITY_OWNER)
        self.powered_up = self.get_tag(GameTag.POWERED_UP)
        self.lettuce_is_equpiment = self.get_tag(GameTag.LETTUCE_IS_EQUPIMENT)
        self.lettuce_is_treasure_card = self.get_tag(GameTag.LETTUCE_IS_TREASURE_CARD)

    def read_from_config(self, d):
        # 从字典读取伤害等参数
        self.damage = d['damage']
        self.range = d['range']
        pass

    def can_use(self):
        # 不是装备且冷却为0
        return self.lettuce_current_cooldown == 0 and not self.lettuce_is_equpiment and not self.lettuce_is_treasure_card

    def play(self, hero, target):
        power = self.game_entity.get_spell_power(self.spell_school)
        # print(power)
        if target is None:
            range = self.range
            if range == 'A':
                hero_list = self.game_entity.get_hero_list(not hero.own())
                for h in hero_list:
                    h.damage += (self.damage + power) * self.damage_advantage[hero.lettuce_role][h.lettuce_role]
                pass
            elif int(range) < 0:
                range = int(range)
                hero_list = self.game_entity.get_hero_list(not hero.own())
                range = -range
                hero_list = random.sample(hero_list, range)
                for h in hero_list:
                    h.damage += (self.damage + power) * self.damage_advantage[hero.lettuce_role][h.lettuce_role]
                pass
        else:
            target.damage += (self.damage + power) * self.damage_advantage[hero.lettuce_role][target.lettuce_role]

        pass

    def damage_trigger(self, target):
        # 受伤触发器

        pass

    def __lt__(self, other):
        return self.cost < other.cost or not self.combo

    def __str__(self):
        return {'card_id': self.card_id, 'damage': self.damage, 'cost': self.cost, 'range': self.range,
                'cooldown': self.lettuce_current_cooldown}.__str__()
