# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_471(SpellEntity):
    """
        纠缠根须5
        对一个敌人造成$16点伤害并<b>缠绕</b>目标。0对一个敌人造成$16点伤害并<b>缠绕</b>目标。其下一个技能的速度值减慢（1）点。0对一个敌人造成$16点伤害并<b>缠绕</b>目标。其下一个技能的速度值减慢（2）点。0对一个敌人造成$16点伤害并<b>缠绕</b>目标。其下一个技能的速度值减慢（3）点。0对一个敌人造成$16点伤害并<b>缠绕</b>目标。其下一个技能的速度值减慢（4）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

