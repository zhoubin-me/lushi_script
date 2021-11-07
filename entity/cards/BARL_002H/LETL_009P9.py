# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_009P9(SpellEntity):
    """
        动员打击5
        <b>攻击</b>一个敌人。使你的所有受伤的兽人获得+3/+5。0<b>攻击</b>一个敌人。使你的所有受伤的兽人获得+4/+6。0<b>攻击</b>一个敌人。使你的所有受伤的兽人获得+5/+7。0<b>攻击</b>一个敌人。使你的所有受伤的兽人获得+6/+8。0<b>攻击</b>一个敌人。使你的所有受伤的兽人获得+7/+9。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

