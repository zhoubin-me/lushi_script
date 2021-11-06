# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_392(SpellEntity):
    """
        保护兽群3
        在本回合中获得<b>嘲讽</b>。每当此佣兵受到<b>攻击</b>时，获得+10生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

