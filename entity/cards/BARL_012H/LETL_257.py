# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_257(SpellEntity):
    """
        邪能抽笞5
        对一个敌人造成$10点伤害，并使其在本回合中无法恢复。0对一个敌人造成$13点伤害，并使其在本回合中无法恢复。0对一个敌人造成$14点伤害，并使其在本回合中无法恢复。0对一个敌人造成$15点伤害，并使其在本回合中无法恢复。0对一个敌人造成$16点伤害，并使其在本回合中无法恢复。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

