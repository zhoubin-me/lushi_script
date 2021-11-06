from typing import List, Any

from hearthstone.entities import Entity
from hearthstone.enums import GameTag, SpellSchool

from .base_entity import BaseEntity
from .spell_entity import SpellEntity


class HeroEntity(BaseEntity):

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.card_id = '1'
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
        # 被动 一技能 二技能 三技能 ...
        self.spell: List[SpellEntity] = []
        # 法术伤害
        self.spellpower = {
            SpellSchool.NONE: 0,  # 无
            SpellSchool.ARCANE: 0,  # 奥术
            SpellSchool.FIRE: 0,  # 火焰
            SpellSchool.FROST: 0,  # 冰霜
            SpellSchool.NATURE: 0,  # 自然
            SpellSchool.HOLY: 0,  # 神圣
            SpellSchool.SHADOW: 0,  # 暗影
            SpellSchool.FEL: 0,  # 邪能
            SpellSchool.PHYSICAL_COMBAT: 0
        }

        # 受伤触发器
        self.damage_trigger: List[SpellEntity] = []

        self.deathrattle = 0
        # 是否选择了技能
        self.lettuce_has_manually_selected_ability = 0
        # 选了什么技能
        self.lettuce_ability_tile_visual_self_only = 0
        # 敌方选择的技能entity_id
        self.lettuce_ability_tile_visual_all_visible = 0
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

        self.spellpower[SpellSchool.ARCANE] = self.get_tag(GameTag.SPELLPOWER_ARCANE)
        self.spellpower[SpellSchool.FIRE] = self.get_tag(GameTag.SPELLPOWER_FIRE)
        self.spellpower[SpellSchool.FROST] = self.get_tag(GameTag.SPELLPOWER_FROST)
        self.spellpower[SpellSchool.NATURE] = self.get_tag(GameTag.SPELLPOWER_NATURE)
        self.spellpower[SpellSchool.HOLY] = self.get_tag(GameTag.SPELLPOWER_HOLY)
        self.spellpower[SpellSchool.SHADOW] = self.get_tag(GameTag.SPELLPOWER_SHADOW)
        self.spellpower[SpellSchool.FEL] = self.get_tag(GameTag.SPELLPOWER_FEL)

        self.deathrattle = self.get_tag(GameTag.DEATHRATTLE)
        self.lettuce_has_manually_selected_ability = self.get_tag(GameTag.LETTUCE_HAS_MANUALLY_SELECTED_ABILITY)
        self.lettuce_ability_tile_visual_self_only = self.get_tag(GameTag.LETTUCE_ABILITY_TILE_VISUAL_SELF_ONLY)
        self.lettuce_selected_target = self.get_tag(GameTag.LETTUCE_SELECTED_TARGET)
        self.lettuce_mercenary_experience = self.get_tag(GameTag.LETTUCE_MERCENARY_EXPERIENCE)
        self.lettuce_ability_tile_visual_all_visible = self.get_tag(GameTag.LETTUCE_ABILITY_TILE_VISUAL_ALL_VISIBLE)

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
        if spell.lettuce_is_equpiment:
            spell.equip(self)
        self.spell.append(spell)

    def get_health(self):
        return self.max_health - self.damage

    def basic_attack(self, target, dmg):
        total_dmg = dmg * BaseEntity.damage_advantage[self.lettuce_role][target.lettuce_role]
        target.damage += total_dmg
        return total_dmg

    def get_available_spell_list(self):
        spell_list = [s for s in self.spell if s.can_use()]
        return spell_list

    def get_spell_by_eid(self, entity_id):
        spell = [x for x in self.spell if x.entity_id == entity_id][0]
        return spell

    def get_spell_by_cid(self, card_id):
        spell = [x for x in self.spell if x.compare_card_id(card_id)][0]
        return spell

    def get_enemy_action(self):
        return self.get_spell_by_eid(self.lettuce_ability_tile_visual_all_visible)

    def is_alive(self):
        return self.get_health() > 0

    def got_damage(self, game, damage):
        self.damage += damage
        for spell in self.damage_trigger:
            spell.damage_trigger(game, self)

    def is_adjacent(self, target):
        return abs(self.zone_position - target.zone_position) <= 1

    def compare_card_id(self, card_id):
        return self.card_id.startswith(card_id)

    def __str__(self):
        return {'card_id': self.card_id, 'atk': self.atk, 'health': self.get_health(),
                'zone_pos': self.zone_position}.__str__()
