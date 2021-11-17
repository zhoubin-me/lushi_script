# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_447(SpellEntity):
    """
        萨弗拉斯4
        <b>被动：</b>+20生命值。你的角色无法被<b>冻结</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            