# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_056(SpellEntity):
    """
        寒冬集结
        获得<b>+3冰霜伤害</b>。<b>火焰伤害</b>会移除此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

