# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_281(SpellEntity):
    """
        吞噬5
        吃掉你生命值最低的鱼人并获得其属性值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

