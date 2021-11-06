# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_022P1(SpellEntity):
    """
        魔法乌鸦3
        <b>突袭</b>，<b>战吼：</b>在本局对战中你每施放过一个奥术技能，便获得+3攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

