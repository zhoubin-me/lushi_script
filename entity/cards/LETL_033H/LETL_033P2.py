# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_033P2(SpellEntity):
    """
        屠龙射击5
        造成$10点伤害。如果目标是龙，则改为造成$25点伤害。0造成$12点伤害。如果目标是龙，则改为造成$27点伤害。0造成$13点伤害。如果目标是龙，则改为造成$28点伤害。0造成$14点伤害。如果目标是龙，则改为造成$29点伤害。0造成$15点伤害。如果目标是龙，则改为造成$30点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

