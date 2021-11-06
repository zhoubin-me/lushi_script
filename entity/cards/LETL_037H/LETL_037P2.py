# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_037P2(SpellEntity):
    """
        惊骇5
        你每有一只野兽，便获得+5攻击力。随机<b>攻击</b>一个敌人。0你每有一只野兽，便获得+6攻击力。随机<b>攻击</b>一个敌人。0你每有一只野兽，便获得+7攻击力。随机<b>攻击</b>一个敌人。0你每有一只野兽，便获得+8攻击力。随机<b>攻击</b>一个敌人。0你每有一只野兽，便获得+9攻击力。随机<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

