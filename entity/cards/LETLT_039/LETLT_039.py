# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_039(SpellEntity):
    """
        巨熊之爪
        <b>攻击</b>一个敌人，同时对相邻的敌人造成伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

