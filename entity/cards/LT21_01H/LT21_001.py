# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_001(SpellEntity):
    """
        刺客之刃5
        <b>攻击</b>一个敌人。如果目标在本回合中还没有行动，则获得+5生命值并再次<b>攻击</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

