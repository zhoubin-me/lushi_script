# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_653(SpellEntity):
    """
        法力魔棒4
        奥术箭额外获得<b>+4奥术伤害</b>，但具有+1冷却。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            