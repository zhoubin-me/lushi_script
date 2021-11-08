# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_644(SpellEntity):
    """
        恶魔斗篷4
        <b>被动：</b><b>攻击</b>时受到的伤害降低5点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            