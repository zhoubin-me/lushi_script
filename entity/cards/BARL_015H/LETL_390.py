# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_390(SpellEntity):
    """
        狂暴攻击3
        攻击一个敌人。如果目标在本回合中受到过伤害，则获得+3攻击力并再次攻击。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

