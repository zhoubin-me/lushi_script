# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_622(SpellEntity):
    """
        毁灭之锤4
        <b>被动：</b>+4攻击力及<b>风怒</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            