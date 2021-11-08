# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_266(SpellEntity):
    """
        熊妈妈之爪4
        <b>被动：</b>每当你召唤一只野兽时，使其获得+4/+4。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            