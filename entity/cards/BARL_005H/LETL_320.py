# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_320(SpellEntity):
    """
        暗影震击5
        对一个敌人造成$12点伤害。目标的下一个技能速度值减慢（5）点。0对一个敌人造成$14点伤害。目标的下一个技能速度值减慢（5）点。0对一个敌人造成$15点伤害。目标的下一个技能速度值减慢（5）点。0对一个敌人造成$16点伤害。目标的下一个技能速度值减慢（5）点。0对一个敌人造成$17点伤害。目标的下一个技能速度值减慢（5）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

