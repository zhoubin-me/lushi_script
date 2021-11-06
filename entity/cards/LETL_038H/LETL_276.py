# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_276(SpellEntity):
    """
        原始之力5
        使一只友方野兽获得+15攻击力，且在本回合中<b>攻击</b>时具有<b>免疫</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

