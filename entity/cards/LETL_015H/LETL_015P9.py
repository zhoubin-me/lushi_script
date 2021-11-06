# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_015P9(SpellEntity):
    """
        爆炸射击5
        对一个敌人造成$16点伤害，并对相邻的敌人造成$8点伤害。0对一个敌人造成$17点伤害，并对相邻的敌人造成$9点伤害。0对一个敌人造成$18点伤害，并对相邻的敌人造成$10点伤害。0对一个敌人造成$19点伤害，并对相邻的敌人造成$11点伤害。0对一个敌人造成$20点伤害，并对相邻的敌人造成$12点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

