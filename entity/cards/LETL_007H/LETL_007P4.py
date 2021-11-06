# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_007P4(SpellEntity):
    """
        眼棱5
        造成$12点伤害，为此佣兵恢复等量的生命值。0造成$15点伤害，为此佣兵恢复等量的生命值。0造成$16点伤害，为此佣兵恢复等量的生命值。0造成$17点伤害，为此佣兵恢复等量的生命值。0造成$18点伤害，为此佣兵恢复等量的生命值。0造成$12点伤害，为此佣兵恢复等量的生命值。获得<b>+1邪能伤害</b>。0造成$12点伤害，为此佣兵恢复等量的生命值。获得<b>+2邪能伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

