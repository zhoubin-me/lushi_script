# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_318(SpellEntity):
    """
        寒冰之盾5
        在本回合中获得<b>嘲讽</b>。在一个敌人<b>攻击</b>此佣兵后，将其<b>冻结</b>，直到下回合结束。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

