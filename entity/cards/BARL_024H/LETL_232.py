# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_232(SpellEntity):
    """
        二连击5
        <b>攻击</b>一个敌人。如果目标在本回合中受到过伤害，则获得+5攻击力并再次<b>攻击</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

