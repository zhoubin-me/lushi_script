# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_082(SpellEntity):
    """
        召唤熔岩爪牙
        召唤一或两个会在回合结束时随机攻击并死亡的熔岩爪牙。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

