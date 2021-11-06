# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_005P4(SpellEntity):
    """
        魔爆术5
        对所有敌人造成$8点伤害。0对所有敌人造成$9点伤害。0对所有敌人造成$10点伤害。0对所有敌人造成$11点伤害。0对所有敌人造成$12点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 8
        self.range = 7

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        hero_list = game.get_hero_list(not hero.own())
        for h in hero_list:
            h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][h.lettuce_role])
        pass
