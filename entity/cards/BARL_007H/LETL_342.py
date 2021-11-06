# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_342(SpellEntity):
    """
        野兽恢复5
        为一个角色恢复#15点生命值。如果目标是野兽，还会使其获得+15生命值。0为一个角色和此佣兵恢复#15点生命值。如果目标是野兽，还会使其获得+15生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

