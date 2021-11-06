# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_034P3(SpellEntity):
    """
        先祖勾拳5
        <b>攻击</b>一个敌人。每有一个尚未行动的敌人，便恢复#8点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

