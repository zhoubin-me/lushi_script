# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_254(SpellEntity):
    """
        邪能魔肺4
        恐惧嚎叫还会对所有敌人造成5点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            