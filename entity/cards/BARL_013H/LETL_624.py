# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_624(SpellEntity):
    """
        兽人的旗帜4
        战斗怒吼还会为你的兽人恢复10点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            