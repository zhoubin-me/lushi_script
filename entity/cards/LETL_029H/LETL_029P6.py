# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_029P6(SpellEntity):
    """
        闪电链5
        对一个敌人造成$16点伤害。额外对1个相邻敌人重复此效果。0对一个敌人造成$16点伤害。额外对2个相邻敌人重复此效果。0对一个敌人造成$16点伤害。额外对3个相邻敌人重复此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

