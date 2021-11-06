# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_007P7(SpellEntity):
    """
        屠魔者5
        <b>攻击</b>一个敌人。如果目标是恶魔，则先获得+6攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

