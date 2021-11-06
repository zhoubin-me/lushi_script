# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_024P2(SpellEntity):
    """
        准备火炮5
        在此佣兵的左侧或右侧召唤一门火炮。<i>（开始时为冷却。）</i>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

