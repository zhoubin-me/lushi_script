# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_307(SpellEntity):
    """
        急速冰冻5
        对所有敌人造成$8点伤害。<b>击杀：冻结</b>所有敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

