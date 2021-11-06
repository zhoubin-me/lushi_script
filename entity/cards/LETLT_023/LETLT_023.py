# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_023(SpellEntity):
    """
        古树知识
        为相邻的角色恢复0点生命值，并使其下一个技能的速度值加快（1）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

