# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_487(SpellEntity):
    """
        龙爪之拳4
        <b>被动：</b>战场上有敌方的龙时，格鲁尔便具有+15攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            