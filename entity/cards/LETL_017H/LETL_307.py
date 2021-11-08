# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_307(SpellEntity):
    """
        急速冰冻5
        对所有敌人造成$8点伤害。<b>击杀：冻结</b>所有敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 8
        self.range = 7

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        hero_list = game.get_hero_list(not hero.own())
        for i, h in enumerate(hero_list):
            h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][h.lettuce_role])
