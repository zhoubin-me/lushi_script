# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_711(SpellEntity):
    """
        双刃匕首4
        刀扇使你的其他佣兵速度值额外加快（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            