# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_005P3(SpellEntity):
    """
        陨石术5
        对一个角色造成$25点伤害，并对其相邻角色造成$10点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

