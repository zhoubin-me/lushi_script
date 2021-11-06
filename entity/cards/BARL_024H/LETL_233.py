# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_233(SpellEntity):
    """
        镜像5
        选择一个敌人。召唤此佣兵的一个复制并使复制<b>攻击</b>目标。复制会在回合结束时死亡。0选择一个敌人。召唤此佣兵的两个复制并使复制<b>攻击</b>目标。复制会在回合结束时死亡。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

