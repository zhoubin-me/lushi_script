# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_019(SpellEntity):
    """
        重拳猛击5
        每有一个生命值小于或等于40点的敌人，获得+5攻击力。<b>攻击</b>一个敌人。0每有一个生命值小于或等于40点的敌人，获得+5攻击力。额外获得+1攻击力。<b>攻击</b>一个敌人。0每有一个生命值小于或等于40点的敌人，获得+5攻击力。额外获得+2攻击力。<b>攻击</b>一个敌人。0每有一个生命值小于或等于40点的敌人，获得+5攻击力。额外获得+3攻击力。<b>攻击</b>一个敌人。0每有一个生命值小于或等于50点的敌人，获得+5攻击力。额外获得+4攻击力。<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

