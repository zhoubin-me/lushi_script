# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_005P8(SpellEntity):
    """
        奥术箭5
        造成$12点伤害。获得<b>+3奥术伤害</b>0造成$12点伤害。获得<b>+4奥术伤害</b>0造成$12点伤害。获得<b>+5奥术伤害</b>0造成$12点伤害。获得<b>+6奥术伤害</b>0造成$12点伤害。获得<b>+7奥术伤害</b>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 12
        self.range = 1

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        target.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][target.lettuce_role])

