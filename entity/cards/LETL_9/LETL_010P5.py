# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_010P5(SpellEntity):
    """
        刺骨5
        造成$10点伤害。<b>连击：</b>改为造成$18点。0造成$11点伤害。<b>连击：</b>改为造成$19点。0造成$12点伤害。<b>连击：</b>改为造成$20点。0造成$13点伤害。<b>连击：</b>改为造成$21点。0造成$14点伤害。<b>连击：</b>改为造成$22点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

