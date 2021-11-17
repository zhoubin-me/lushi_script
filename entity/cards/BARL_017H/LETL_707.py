# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_707(SpellEntity):
    """
        活根草之杖4
        <b>被动：</b>每当你施放一个自然技能时，为你的角色恢复#6点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            