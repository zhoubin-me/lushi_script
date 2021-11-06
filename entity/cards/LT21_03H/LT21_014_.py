# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_014_(SpellEntity):
    """
        启动电锯5
        获得+6点攻击力，持续2回合。随机<b>攻击</b>一个敌人。0获得+7点攻击力，持续3回合。随机<b>攻击</b>一个敌人。0获得+8点攻击力，持续3回合。随机<b>攻击</b>一个敌人。0获得+9点攻击力，持续3回合。随机<b>攻击</b>一个敌人。0获得+10点攻击力，持续3回合。随机<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

