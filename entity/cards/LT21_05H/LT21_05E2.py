# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_05E2(SpellEntity):
    """
        开胃前菜4
        <b>对战开始时：</b>使友方角色获得+9生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            