# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_713(SpellEntity):
    """
        狩猎篷布4
        捕熊陷阱的熊具有+5攻击力和<b>突袭</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            