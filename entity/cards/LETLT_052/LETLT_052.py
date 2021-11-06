# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_052(SpellEntity):
    """
        冰风吼叫
        在本回合中，将所有具有<b>嘲讽</b>的敌人的攻击力变为0点。<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

