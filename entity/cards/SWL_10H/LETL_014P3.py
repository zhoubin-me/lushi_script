# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_014P3(SpellEntity):
    """
        神圣新星5
        对所有敌人造成$10点伤害。为你的角色恢复#14点生命值。0对所有敌人造成$12点伤害。为你的角色恢复#14点生命值。0对所有敌人造成$13点伤害。为你的角色恢复#14点生命值。0对所有敌人造成$14点伤害。为你的角色恢复#14点生命值。0对所有敌人造成$15点伤害。为你的角色恢复#14点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass
