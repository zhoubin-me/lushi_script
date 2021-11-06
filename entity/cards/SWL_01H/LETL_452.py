# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_452(SpellEntity):
    """
        火球风暴5
        随机对一个敌人施放火球术5。在本回合中你每施放过一个火焰技能，重复一次。0随机对两个敌人施放火球术5。在本回合中你每施放过一个火焰技能，重复一次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

