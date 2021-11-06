# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_014P2(SpellEntity):
    """
        裂解之光5
        对一个敌人造成$15点伤害。<b>神圣连击</b>：并对相邻的角色造成伤害。0对一个敌人造成$16点伤害。<b>神圣连击</b>：并对相邻的角色造成伤害。0对一个敌人造成$17点伤害。<b>神圣连击</b>：并对相邻的角色造成伤害。0对一个敌人造成$18点伤害。<b>神圣连击</b>：并对相邻的角色造成伤害。0对一个敌人造成$19点伤害。<b>神圣连击</b>：并对相邻的角色造成伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

