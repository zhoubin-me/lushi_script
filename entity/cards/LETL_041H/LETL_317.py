# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_317(SpellEntity):
    """
        凋零缠绕5
        对一个敌人造成$18点伤害，或者为一个友方角色恢复#30点生命值。0对一个敌人造成$18点伤害，或者为一个友方角色恢复#30点生命值。为此佣兵恢复#4点生命值。0对一个敌人造成$18点伤害，或者为一个友方角色恢复#30点生命值。为此佣兵恢复#6点生命值。0对一个敌人造成$18点伤害，或者为一个友方角色恢复#30点生命值。为此佣兵恢复#8点生命值。0对一个敌人造成$18点伤害，或者为一个友方角色恢复#30点生命值。为此佣兵恢复#10点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

