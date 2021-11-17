# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_689(SpellEntity):
    """
        霜之哀伤4
        寒冰之噬还会减慢目标相邻的角色的速度值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            