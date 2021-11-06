# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_002P3(SpellEntity):
    """
        谦逊制裁5
        在本回合中使一个敌人的攻击力变为1点。<b>攻击</b>该敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

