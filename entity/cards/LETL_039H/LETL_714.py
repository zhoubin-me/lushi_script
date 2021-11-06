# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_714(SpellEntity):
    """
        拉线操纵4
        <b>被动：</b>+10生命值。你的陷阱会一直存在，直到被触发。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            