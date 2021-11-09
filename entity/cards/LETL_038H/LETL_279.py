# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_279(SpellEntity):
    """
        穆克拉的大表哥4
        <b>战吼：</b>召唤一只12/24并具有<b>嘲讽</b>的野兽。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            