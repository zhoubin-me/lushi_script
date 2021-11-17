# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_643(SpellEntity):
    """
        埃辛诺斯战刃4
        流放攻击还会<b>攻击</b>最左边的敌人两次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            