# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_030P4(SpellEntity):
    """
        活体炸弹
        选择一个敌人。如果目标在本回合中受到伤害，则对目标和相邻的角色造成12点伤害
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 12
        self.combo_damage = 8
        self.range = 1
        self.trigger_twice = 1

    def play(self, hero, target):
        target.damage_trigger.append(self)
        pass

    def damage_trigger(self, target):
        power = self.game_entity.get_spell_power(self.spell_school, target.own)

        hero_list = self.game_entity.get_hero_list(target.own())
        for h in hero_list:
            if target.is_adjacent(h):
                h.got_damage(self.damage + power)
                if self.trigger_twice:
                    h.got_damage(self.damage + power)
