# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_05P3(SpellEntity):
    """
        鱼类大餐5
        对一个敌人造成${0}点伤害。<b>击杀</b>：使所有友方角色获得+{1}生命值。10对一个敌人造成${0}点伤害。<b>击杀</b>：使所有友方角色获得+2/+{1}。10对一个敌人造成${0}点伤害。<b>击杀</b>：使所有友方角色获得+3/+{1}。10对一个敌人造成${0}点伤害。<b>击杀</b>：使所有友方角色获得+4/+{1}。10对一个敌人造成${0}点伤害。<b>击杀</b>：使所有友方角色获得+5/+{1}。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

