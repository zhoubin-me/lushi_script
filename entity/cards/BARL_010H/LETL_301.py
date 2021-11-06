# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_301(SpellEntity):
    """
        生命虹吸5
        造成$12点伤害。为所有友方兽人和恶魔恢复等量的生命值。0造成$13点伤害。为所有友方兽人和恶魔恢复等量的生命值。0造成$14点伤害。为所有友方兽人和恶魔恢复等量的生命值。0造成$15点伤害。为所有友方兽人和恶魔恢复等量的生命值。0造成$16点伤害。为所有友方兽人和恶魔恢复等量的生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

