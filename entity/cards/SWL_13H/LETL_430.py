# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_430(SpellEntity):
    """
        保护祝福5
        为一个友方角色恢复#10点生命值，并使其在本回合中获得<b>嘲讽</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

