# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_028P11(SpellEntity):
    """
        熔岩冲击5
        造成$10点伤害。<b>火焰连击：</b>改为造成$18点伤害。0造成$12点伤害。<b>火焰连击：</b>改为造成$20点伤害。0造成$13点伤害。<b>火焰连击：</b>改为造成$21点伤害。0造成$14点伤害。<b>火焰连击：</b>改为造成$22点伤害。0造成$15点伤害。<b>火焰连击：</b>改为造成$23点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

