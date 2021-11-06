# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_669(SpellEntity):
    """
        寒冰屏障护身符4
        <b>被动：</b>当此佣兵第一次即将承受致命伤害时，防止这些伤害，并使其在本回合中获得<b>免疫</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            