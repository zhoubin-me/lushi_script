# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_029P5(SpellEntity):
    """
        闪电箭5
        造成$10点伤害。获得<b>+3自然伤害</b>0造成$11点伤害。获得<b>+3自然伤害</b>0造成$12点伤害。获得<b>+3自然伤害</b>0造成$13点伤害。获得<b>+3自然伤害</b>0造成$14点伤害。获得<b>+3自然伤害</b>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

