# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_250(SpellEntity):
    """
        奔跑破坏神5
        <b>攻击</b>一个敌人。使你的恶魔获得+8生命值。0<b>攻击</b>一个敌人。使你的恶魔获得+10生命值。0<b>攻击</b>一个敌人。使你的恶魔获得+11生命值。0<b>攻击</b>一个敌人。使你的恶魔获得+12生命值。0<b>攻击</b>一个敌人。使你的恶魔获得+13生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

