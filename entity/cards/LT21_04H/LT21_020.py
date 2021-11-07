# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_020(SpellEntity):
    """
        停火5
        在本回合中获得<b>嘲讽</b>。在敌人<b>攻击</b>此佣兵后，获得+5攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

