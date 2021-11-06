# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_316(SpellEntity):
    """
        寒冰之噬5
        <b>攻击</b>一个敌人，并使其在本回合中施放的技能速度值永久减慢（5）点。0<b>攻击</b>一个敌人，同时使其和相邻敌人在本回合中施放的技能速度值永久减慢（5）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

