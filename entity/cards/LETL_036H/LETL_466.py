# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_466(SpellEntity):
    """
        土灵护腕4
        铁木树皮额外获得+2/+4。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            