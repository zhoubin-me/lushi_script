# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_436(SpellEntity):
    """
        牺牲圣契4
        <b>亡语：</b>使你的角色获得<b>圣盾</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            