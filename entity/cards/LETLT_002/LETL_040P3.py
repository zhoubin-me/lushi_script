# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_040P3(SpellEntity):
    """
        暗影箭5
        造成$13点伤害。0造成$14点伤害。0造成$15点伤害。0造成$16点伤害。0造成$17点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

