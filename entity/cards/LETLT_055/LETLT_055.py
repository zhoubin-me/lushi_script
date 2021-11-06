# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_055(SpellEntity):
    """
        冰刃锋缘
        获得<b>+3冰霜伤害</b>。<b>火焰伤害</b>会移除此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

