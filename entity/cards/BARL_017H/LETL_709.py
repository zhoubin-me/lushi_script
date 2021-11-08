# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_709(SpellEntity):
    """
        森林徽章4
        纠缠根须还会使敌人下一个技能的速度值减慢（4）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            