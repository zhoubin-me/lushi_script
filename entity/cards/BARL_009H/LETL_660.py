# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_660(SpellEntity):
    """
        巨龙之爪4
        辟法巨龙具有+5攻击力及<b>风怒</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            