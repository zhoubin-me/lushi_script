# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_081(SpellEntity):
    """
        岩石与火焰之盾
        获得<b>嘲讽</b>。在本回合中，每次受到攻击前，攻击力翻倍。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

