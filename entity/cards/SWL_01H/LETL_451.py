# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_451(SpellEntity):
    """
        烈焰风暴5
        对所有敌人造成$14点伤害。0对所有敌人造成$16点伤害。0对所有敌人造成$17点伤害。0对所有敌人造成$18点伤害。0对所有敌人造成$19点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 14
        self.range = 7

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        hero_list = game.get_hero_list(not hero.own())
        for h in hero_list:
            h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][h.lettuce_role])
