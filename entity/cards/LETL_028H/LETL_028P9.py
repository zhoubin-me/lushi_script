# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_028P9(SpellEntity):
    """
        死吧，虫子5
        随机对一个敌人造成$22点伤害。<b>击杀：</b>重复此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 22
        self.range = -1

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        # 随机只打血最高
        h = game.find_max_health(not hero.own())
        h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][h.lettuce_role])
        while not h.is_alive():
            h = game.find_max_health(not hero.own())
            if h.get_health() <= 0:
                break
            h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][h.lettuce_role])
