# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_703(SpellEntity):
    """
        引雷针4
        闪电链额外对两个敌人重复，但具有+1冷却。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            