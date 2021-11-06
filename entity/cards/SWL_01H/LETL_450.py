# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_450(SpellEntity):
    """
        火球术5
        造成$12点伤害。0造成$13点伤害。0造成$14点伤害。0造成$15点伤害。0造成$16点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 12
        self.range = 1

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        target.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][target.lettuce_role])


