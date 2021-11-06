# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_027P6(SpellEntity):
    """
        鱼人飞弹5
        造成$10点伤害。使你的鱼人获得+5生命值。0造成$10点伤害。使你的队伍获得+5生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

