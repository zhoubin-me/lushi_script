# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_073p1(SpellEntity):
    """
        龙人打击
        <b>攻击</b>一个敌人。如果目标的生命值更低，则先获得+{0}/+{0}。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

