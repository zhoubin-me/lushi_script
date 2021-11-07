# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_407(SpellEntity):
    """
        快速治疗5
        恢复#15点生命值。0恢复#20点生命值。0恢复#25点生命值。0恢复#30点生命值。0恢复#35点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

