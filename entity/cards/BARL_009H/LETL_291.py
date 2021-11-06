# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_291(SpellEntity):
    """
        辟法巨龙5
        <b>圣盾</b>，<b>突袭</b>@<b>圣盾</b>，<b>突袭</b>，<b>风怒</b>@<b>圣盾</b>，<b>突袭</b>，<b>风怒</b>@<b>圣盾</b>，<b>突袭</b>，<b>风怒</b>@<b>圣盾</b>，<b>突袭</b>，<b>风怒</b>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

