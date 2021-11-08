# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_608(SpellEntity):
    """
        泡泡魔杖4
        鱼人入侵还会使此佣兵获得+5攻击力和<b>圣盾</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            