# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_076p1(SpellEntity):
    """
        火山之焰
        随机对一个敌人造成$0点伤害。在本局对战中每有一个角色死亡，重复一次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

