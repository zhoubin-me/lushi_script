# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_043(SpellEntity):
    """
        熊怪的挑战
        <b>攻击</b>一个敌人。如果目标尚未行动，则获得<b>嘲讽</b>1回合。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

