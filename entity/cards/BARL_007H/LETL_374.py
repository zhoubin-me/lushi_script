# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_374(SpellEntity):
    """
        毒蛇点心4
        梦魇毒蛇具有+10生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            