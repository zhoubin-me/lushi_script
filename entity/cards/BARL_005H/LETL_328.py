# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_328(SpellEntity):
    """
        虚弱诅咒5
        在本回合中，使所有敌人获得<b>+6暗影虚弱</b>，并对其造成$8点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

