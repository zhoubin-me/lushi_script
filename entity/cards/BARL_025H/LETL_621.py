# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_621(SpellEntity):
    """
        力量之戒4
        <b>被动：</b>每当一个友方兽人受到<b>攻击</b>时，使其获得+8生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            