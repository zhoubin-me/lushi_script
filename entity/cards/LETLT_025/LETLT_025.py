# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_025(SpellEntity):
    """
        古树的坚韧
        获得<b>嘲讽</b>1回合。每有一个友方角色，获得+{0}/+{0}。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

