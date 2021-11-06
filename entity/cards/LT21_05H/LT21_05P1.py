# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_05P1(SpellEntity):
    """
        曲奇下厨5
        使所有敌人<b>流血(${0})</b>。为友方鱼人和海盗恢复{1}点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

