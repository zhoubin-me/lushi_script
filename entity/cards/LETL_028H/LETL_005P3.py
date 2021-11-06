# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_005P3(SpellEntity):
    """
        陨石术5
        对一个角色造成$25点伤害，并对其相邻角色造成$10点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 25
        self.damage2 = 10
        self.range = 1

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, target.own)
        hero_list = game.get_hero_list(target.own())
        for h in hero_list:
            if target.is_adjacent(h):
                # 是自己
                if target.entity_id == h.entity_id:
                    h.got_damage(game, self.damage + power)
                else:
                    h.got_damage(game, self.damage2 + power)
