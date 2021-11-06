# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_033P5(SpellEntity):
    """
        癫狂乱舞5
        <b>攻击</b>一个敌人。如果此佣兵在本回合中受到了伤害，则先获得+6攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

