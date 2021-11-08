# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_305(SpellEntity):
    """
        混乱之杖4
        <b>被动：</b>在一个兽人死亡后，获得<b>+4邪能伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            