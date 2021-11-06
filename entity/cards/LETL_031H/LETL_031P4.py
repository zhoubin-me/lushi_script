# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_031P4(SpellEntity):
    """
        烈焰猛击5
        对一个敌人造成$16点伤害。如果你控制着另一条龙，则对相邻的敌人同样造成伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

