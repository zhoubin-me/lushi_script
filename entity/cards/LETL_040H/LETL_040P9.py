# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_040P9(SpellEntity):
    """
        暗影之幕5
        获得<b>+5暗影伤害</b>。在本回合中，敌人无法恢复。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

