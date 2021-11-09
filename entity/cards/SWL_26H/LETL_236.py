# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_236(SpellEntity):
    """
        火焰践踏5
        对所有敌人造成$6点伤害。每有一个尚未行动的敌人，重复一次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 6
        self.range = 7

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        # 获取技能列表
        action_list = game.get_action_list(not hero.own)
        action_list.sort()
        # self.cost 这个技能的速度,
        cnt = 0
        for action in action_list:
            if action.spell.cost >= self.cost:
                # 假设同速下，我方先使用技能
                cnt += 1
        hero_list = game.get_hero_list(not hero.own())
        for i in range(cnt):
            for h in hero_list:
                h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][h.lettuce_role])
