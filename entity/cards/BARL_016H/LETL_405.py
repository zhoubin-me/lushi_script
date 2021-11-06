# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_405(SpellEntity):
    """
        艾露恩的赐福5
        你的下一个奥术技能会施放两次，且速度值永久加快（3）点。0你的下一个奥术或自然技能会施放两次，且速度值永久加快（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

