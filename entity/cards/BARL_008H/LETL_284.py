# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_284(SpellEntity):
    """
        珠光之鳞4
        <b>被动：</b>在一个鱼人死亡后，获得+2/+10。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            