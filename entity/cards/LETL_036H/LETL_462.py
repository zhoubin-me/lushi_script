# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_462(SpellEntity):
    """
        铁木树皮5
        在本回合中获得<b>嘲讽</b>。在本回合中，在你施放一个自然技能后，获得+4/+12。0在本回合中获得<b>嘲讽</b>。在本回合中，在你施放一个自然技能后，获得+5/+14。0在本回合中获得<b>嘲讽</b>。在本回合中，在你施放一个自然技能后，获得+5/+15。0在本回合中获得<b>嘲讽</b>。在本回合中，在你施放一个自然技能后，获得+6/+15。0在本回合中获得<b>嘲讽</b>。在本回合中，在你施放一个自然技能后，获得+6/+16。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

