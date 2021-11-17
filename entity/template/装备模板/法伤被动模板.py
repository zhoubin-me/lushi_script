# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_446_M(SpellEntity):
    """
        炽烧符文4
        <b>被动：</b><b>+3火焰伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        # 被动增加属性的不需要填效果
        pass

            