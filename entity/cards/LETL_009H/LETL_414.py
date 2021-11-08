# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_414(SpellEntity):
    """
        惊愕猛击5
        对一个敌人造成$10点伤害，并使其下一个技能的速度值减慢（6）点。0对一个敌人造成$12点伤害，并使其下一个技能的速度值减慢（6）点。0对一个敌人造成$13点伤害，并使其下一个技能的速度值减慢（6）点。0对一个敌人造成$14点伤害，并使其下一个技能的速度值减慢（6）点。0对一个敌人造成$15点伤害，并使其下一个技能的速度值减慢（6）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

