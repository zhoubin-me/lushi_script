# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_247(SpellEntity):
    """
        迅捷图腾4
        坚韧光环使此佣兵的下一个技能速度值加快（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            