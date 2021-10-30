from typing import List, Any

from hearthstone.entities import Entity
from hearthstone.enums import GameTag

from .base_entity import BaseEntity
from .spell_entity import SpellEntity


class HeroEntity(BaseEntity):

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.card_id = 0
        self.atk = 0
        self.max_health = 0
        # 受伤
        self.damage = 0
        # INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 TANK = 3 NEUTRAL = 4
        self.lettuce_role = 2  # 斗士
        self.cardrace = None
        self.pos = [0, 0]  # 坐标[x, y]
        # 场上位置 从左往右1开始

        self.zone_position = 0
        # 意义不明
        self.cost = 0
        self.divine_shield = 0
        # INVALID = 0 部落HORDE = 1  联盟ALLIANCE = 2 中立NEUTRAL = 3
        self.faction = 0
        self.windfury = 0
        self.spell_cnt = 1
        # 被动 一技能 二技能 三技能 ...
        self.spell: List[SpellEntity] = [None] * 4
        self.spellpower = 0
        self.deathrattle = 0
        # 是否选择了技能
        self.lettuce_has_manually_selected_ability = 0
        # 选了什么技能
        self.lettuce_ability_tile_visual_self_only = 0
        # 技能选择的目标
        self.lettuce_selected_target = 0
        # 经验 55000满级
        self.lettuce_mercenary_experience = 0
        self.skill_seq = None
        self.parse_entity()

    def parse_entity(self):
        if self.entity is None:
            return
        super(HeroEntity, self).parse_entity()
        self.card_id = self.entity.card_id
        self.atk = self.get_tag(GameTag.ATK)
        self.max_health = self.get_tag(GameTag.HEALTH)
        self.damage = self.get_tag(GameTag.DAMAGE)
        self.lettuce_role = self.get_tag(GameTag.LETTUCE_ROLE)
        self.cardrace = self.get_tag(GameTag.CARDRACE)
        self.zone_position = self.get_tag(GameTag.ZONE_POSITION)
        self.cost = self.get_tag(GameTag.COST)
        self.divine_shield = self.get_tag(GameTag.DIVINE_SHIELD)
        self.faction = self.get_tag(GameTag.FACTION)
        self.windfury = self.get_tag(GameTag.WINDFURY)
        self.spellpower = self.get_tag(GameTag.SPELLPOWER)
        self.deathrattle = self.get_tag(GameTag.DEATHRATTLE)
        self.lettuce_has_manually_selected_ability = self.get_tag(GameTag.LETTUCE_HAS_MANUALLY_SELECTED_ABILITY)
        self.lettuce_ability_tile_visual_self_only = self.get_tag(GameTag.LETTUCE_ABILITY_TILE_VISUAL_SELF_ONLY)
        self.lettuce_selected_target = self.get_tag(GameTag.LETTUCE_SELECTED_TARGET)
        self.lettuce_mercenary_experience = self.get_tag(GameTag.LETTUCE_MERCENARY_EXPERIENCE)

    def set_pos(self, x, y):
        self.pos = [x, y]

    def set_skill_seq(self, skills):
        self.skill_seq = skills

    def own(self):
        """
        谁的随从
        """
        return self.controller == 3

    def add_spell(self, spell: SpellEntity):
        self.spell[self.spell_cnt] = spell
        self.spell_cnt = (self.spell_cnt + 1) % 4
        pass

    def get_health(self):
        return self.max_health - self.damage

    def basic_attack(self, target, dmg):
        total_dmg = dmg * BaseEntity.damage_advantage[self.lettuce_role][target.lettuce_role]
        target.damage += total_dmg
        return total_dmg

    def __str__(self):
        return {'card_id': self.card_id, 'atk': self.atk, 'health': self.get_health(),
                'zone_pos': self.zone_position}.__str__()
