# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_245(SpellEntity):
    """
        圣光药水4
        <b>亡语：</b>为你的角色恢复40点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            