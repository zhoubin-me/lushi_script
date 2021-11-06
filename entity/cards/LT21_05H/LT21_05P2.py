# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_05P2(SpellEntity):
    """
        小鱼快冲5
        随机为你的对手召唤一条具有对你有利的<b>亡语</b>的鱼。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

