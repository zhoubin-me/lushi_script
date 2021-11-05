# -*- coding: utf-8 -*-
from hearthstone.entities import Entity
from hearthstone.enums import GameTag, SpellSchool

from entity.spell_entity import SpellEntity


class LETL_030P4(SpellEntity):
    """
        地狱火
        对所有敌人造成8点伤害。火焰连击：再造成8点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 8
        self.combo_damage = 8
        self.range = 7

    def play(self, hero, target):
        power = self.game_entity.get_spell_power(self.spell_school, hero.own)
        action_list = self.game_entity.get_action_list(hero.own)
        action_list.sort()
        combo = self.game_entity.can_combo(self, SpellSchool.FIRE, hero.own)
        combo_damage = (self.combo_damage + power) * combo
        target.got_damage(
            (self.damage + combo_damage + power) * self.damage_advantage[self.lettuce_role][target.lettuce_role])
