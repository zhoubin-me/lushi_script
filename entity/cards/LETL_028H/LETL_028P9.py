# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_028P9(SpellEntity):
    """
        死吧，虫子5
        随机对一个敌人造成$22点伤害。<b>击杀：</b>重复此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

