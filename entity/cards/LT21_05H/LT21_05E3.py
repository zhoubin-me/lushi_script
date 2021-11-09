# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_05E3(SpellEntity):
    """
        调味的锅4
        鱼类大餐还会获得+5攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            