# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_004P1(SpellEntity):
    """
        鳞甲嘲讽5
        在本回合中，获得<b>嘲讽</b>且受到的伤害减少3点。0在本回合中，获得<b>嘲讽</b>且受到的伤害减少4点。0在本回合中，获得<b>嘲讽</b>且受到的伤害减少5点。0在本回合中，获得<b>嘲讽</b>且受到的伤害减少6点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

