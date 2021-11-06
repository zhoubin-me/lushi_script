# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_292(SpellEntity):
    """
        火焰吐息5
        造成$10点伤害。你每控制着一条龙，重复一次。0造成$11点伤害。你每控制着一条龙，重复一次。0造成$12点伤害。你每控制着一条龙，重复一次。0造成$13点伤害。你每控制着一条龙，重复一次。0造成$14点伤害。你每控制着一条龙，重复一次。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

