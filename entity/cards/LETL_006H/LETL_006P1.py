# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_006P1(SpellEntity):
    """
        邪能地狱火5
        <b>+2邪能伤害</b>@<b>+3邪能伤害</b>@<b>+4邪能伤害</b>@<b>+5邪能伤害</b>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

