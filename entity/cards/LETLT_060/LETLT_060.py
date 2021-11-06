# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_060(SpellEntity):
    """
        饥饿寒冰
        所有友方角色会<b>冻结</b>伤害的敌人。<b>火焰伤害</b>会终结此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

