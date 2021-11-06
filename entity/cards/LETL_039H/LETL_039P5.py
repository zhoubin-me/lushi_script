# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_039P5(SpellEntity):
    """
        爆炸陷阱5
        在本回合中，此佣兵第一次受到伤害时，对所有敌人造成$16点伤害。0此佣兵第一次受到伤害时，对所有敌人造成$16点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

