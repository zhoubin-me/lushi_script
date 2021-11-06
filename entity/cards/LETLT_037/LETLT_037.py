# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_037(SpellEntity):
    """
        闪电链
        对一个敌人造成0点伤害。并随机在相邻的敌人身上弹跳两次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

