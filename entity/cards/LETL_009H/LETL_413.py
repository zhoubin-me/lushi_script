# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_413(SpellEntity):
    """
        战斗怒火5
        获得+8攻击力。<b>攻击</b>一个敌人及一个相邻的角色。0获得+9攻击力。<b>攻击</b>一个敌人及一个相邻的角色。0获得+10攻击力。<b>攻击</b>一个敌人及一个相邻的角色。0获得+11攻击力。<b>攻击</b>一个敌人及一个相邻的角色。0获得+12攻击力。<b>攻击</b>一个敌人及一个相邻的角色。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

