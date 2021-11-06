# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_080(SpellEntity):
    """
        炽灼巨口
        <b>攻击</b>一个敌人。使其直到下回合结束时速度值减慢3点，且无法被治疗。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

