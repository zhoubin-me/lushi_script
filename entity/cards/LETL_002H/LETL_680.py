# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_680(SpellEntity):
    """
        灰烬使者4
        <b>亡语：</b>使你战场和后备中的所有佣兵获得+8/+8。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            