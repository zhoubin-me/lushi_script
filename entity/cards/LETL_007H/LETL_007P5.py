# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_007P5(SpellEntity):
    """
        盲目突击5
        随机<b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，便在本回合中获得<b>免疫</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

