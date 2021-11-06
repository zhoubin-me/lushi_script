# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_623(SpellEntity):
    """
        决斗护手4
        如果此佣兵的生命值少于或等于50点，荣耀决斗将战斗至死！
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            