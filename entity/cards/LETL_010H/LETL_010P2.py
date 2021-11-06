# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_010P2(SpellEntity):
    """
        战术打击5
        <b>攻击</b>一个敌人。<b>连击</b>：并对其造成$10点伤害。0<b>攻击</b>一个敌人。<b>连击</b>：并对其造成$11点伤害。0<b>攻击</b>一个敌人。<b>连击</b>：并对其造成$12点伤害。0<b>攻击</b>一个敌人。<b>连击</b>：并对其造成$13点伤害。0<b>攻击</b>一个敌人。<b>连击</b>：并对其造成$14点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

