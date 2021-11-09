# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_424(SpellEntity):
    """
        疗愈长袍4
        <b>被动：</b>在一个友方人类死亡后，刷新圣言术：赎。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            