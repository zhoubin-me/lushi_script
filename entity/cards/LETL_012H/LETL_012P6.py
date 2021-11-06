# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_012P6(SpellEntity):
    """
        英勇飞跃5
        对一个敌人造成$14点伤害。你的其他人类的速度值永久加快（1）点。0对一个敌人造成$16点伤害。你的其他人类的速度值永久加快（1）点。0对一个敌人造成$17点伤害。你的其他人类的速度值永久加快（1）点。0对一个敌人造成$18点伤害。你的其他人类的速度值永久加快（1）点。0对一个敌人造成$19点伤害。你的其他人类的速度值永久加快（1）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

