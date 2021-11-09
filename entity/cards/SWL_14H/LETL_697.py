# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_697(SpellEntity):
    """
        法力符文4
        法力闪现使你的角色下一个技能的速度值加快（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            