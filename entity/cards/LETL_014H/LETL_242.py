# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_242(SpellEntity):
    """
        神圣冲击5
        造成$12点伤害。为你的角色恢复#6点生命值。0造成$12点伤害。为你的角色恢复#8点生命值。0造成$12点伤害。为你的角色恢复#9点生命值。0造成$12点伤害。为你的角色恢复#10点生命值。0造成$12点伤害。为你的角色恢复#11点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

