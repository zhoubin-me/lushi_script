# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_002(SpellEntity):
    """
        首脑的悬赏5
        对一个敌人造成${0}点伤害。你每控制一个其他海盗，重复一次。<b>击杀</b>：恢复{1}点生命值。10对一个敌人造成${0}点伤害。你每控制一个其他海盗，重复一次。<b>击杀</b>：为所有友方海盗恢复{1}点生命值。10对一个敌人造成${0}点伤害。你每控制一个其他海盗，重复一次。<b>击杀</b>：为所有友方角色恢复{1}点生命值。10对一个敌人造成${0}点伤害。你每控制一个其他海盗，重复一次。<b>击杀</b>：为所有友方角色恢复{1}点生命值。10对一个敌人造成${0}点伤害。你每控制一个其他海盗，重复一次。<b>击杀</b>：为所有友方角色恢复{1}点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

