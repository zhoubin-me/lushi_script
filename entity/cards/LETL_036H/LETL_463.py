# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_463(SpellEntity):
    """
        活体荆棘5
        造成$10点伤害。<b>自然连击：</b>重复此效果。0造成$11点伤害。<b>自然连击：</b>重复此效果。0造成$12点伤害。<b>自然连击：</b>重复此效果。0造成$13点伤害。<b>自然连击：</b>重复此效果。0造成$14点伤害。<b>自然连击：</b>重复此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

