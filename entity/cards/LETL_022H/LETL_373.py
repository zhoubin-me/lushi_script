# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_373(SpellEntity):
    """
        守卫冲击3
        对一个敌人造成$8点伤害。<b>奥术连击：</b>并对一个相邻的敌人造成伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

