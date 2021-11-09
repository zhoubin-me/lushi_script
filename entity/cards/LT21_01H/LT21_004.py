# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_004(SpellEntity):
    """
        黑色船旗4
        <b>被动：</b>相邻海盗的速度值加快（4）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            