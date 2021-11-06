# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_666(SpellEntity):
    """
        黑暗灵魂石4
        <b>被动：</b>在一个角色死亡后，此佣兵获得+10生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            