# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_017_(SpellEntity):
    """
        泰坦神铁锯刃4
        启动电锯获得+4攻击力，持续时间增加1回合。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            