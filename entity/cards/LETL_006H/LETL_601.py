# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_601(SpellEntity):
    """
        狂怒坠饰4
        加拉克苏斯之拳造成的伤害增加5点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            