# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_014P1(SpellEntity):
    """
        致盲之光5
        对一个敌人造成$10点伤害，并使其在本回合中获得-8攻击力。0对一个敌人造成$11点伤害，并使其在本回合中获得-9攻击力。0对一个敌人造成$12点伤害，并使其在本回合中获得-10攻击力。0对一个敌人造成$13点伤害，并使其在本回合中获得-11攻击力。0对一个敌人造成$14点伤害，并使其在本回合中获得-12攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

