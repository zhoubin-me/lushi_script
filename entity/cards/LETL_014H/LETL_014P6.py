# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_014P6(SpellEntity):
    """
        维伦的祝福5
        获得<b>+3神圣伤害</b>。你的下一个神圣技能会施放两次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

