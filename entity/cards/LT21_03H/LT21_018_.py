# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_018_(SpellEntity):
    """
        加装锯刃4
        对战开始时斯尼德具有启动电锯5，持续1回合。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            