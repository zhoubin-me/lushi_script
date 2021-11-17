# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_638(SpellEntity):
    """
        燃烧之刃4
        <b>被动：</b>每当此佣兵<b>攻击</b>时，获得+2/+2。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            