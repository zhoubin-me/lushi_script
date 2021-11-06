# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_088(SpellEntity):
    """
        高耸地狱火
        直到下回合结束时，获得<b>嘲讽</b>。在敌人<b>攻击</b>此佣兵后，获得<b>+2火焰伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

