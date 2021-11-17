# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_040P5(SpellEntity):
    """
        最终仪祭4
        <b>亡语：</b>召唤一个25/25并具有<b>嘲讽</b>的虚空守卫。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            