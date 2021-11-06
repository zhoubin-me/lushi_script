# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_409(SpellEntity):
    """
        嘲讽5
        为此佣兵恢复#12点生命值并获得<b>嘲讽</b>，持续3回合。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

