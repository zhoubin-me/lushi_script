# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_027P2(SpellEntity):
    """
        鱼人弹幕5
        随机对一个敌人造成$12点伤害。每有一个你的其他鱼人，重复一次。0随机对一个敌人造成$13点伤害。每有一个你的其他鱼人，重复一次。0随机对一个敌人造成$14点伤害。每有一个你的其他鱼人，重复一次。0随机对一个敌人造成$15点伤害。每有一个你的其他鱼人，重复一次。0随机对一个敌人造成$16点伤害。每有一个你的其他鱼人，重复一次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

