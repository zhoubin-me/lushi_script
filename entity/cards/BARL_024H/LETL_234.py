# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_234(SpellEntity):
    """
        旋风之刃5
        对所有敌人造成$10点伤害。在本回合中获得<b>免疫</b>。0对所有敌人造成$11点伤害。在本回合中获得<b>免疫</b>。0对所有敌人造成$12点伤害。在本回合中获得<b>免疫</b>。0对所有敌人造成$13点伤害。在本回合中获得<b>免疫</b>。0对所有敌人造成$14点伤害。在本回合中获得<b>免疫</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

