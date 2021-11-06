# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_006(SpellEntity):
    """
        轮番豪饮4
        辅助打击的速度值加快（3）点且在<b>攻击</b>时总会具有<b>免疫</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            