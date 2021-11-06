# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_031P2(SpellEntity):
    """
        红龙女王的计策5
        对一个敌人造成等同于其攻击力的伤害。0对一个敌人造成等同于其攻击力的伤害，并为此佣兵恢复等量的生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

