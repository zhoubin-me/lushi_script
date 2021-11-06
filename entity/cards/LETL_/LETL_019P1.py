# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_019P1(SpellEntity):
    """
        致命一击5
        <b>攻击</b>生命值最低的敌人。<b>连击：</b>先获得+10攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

