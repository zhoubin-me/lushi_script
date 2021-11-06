# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_085(SpellEntity):
    """
        延烧之火
        引燃一个敌人，对一个敌人造成$3点伤害，并在回合结束时传播到一个相邻角色身上。<i>（治疗可以移除此效果。）</i>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

