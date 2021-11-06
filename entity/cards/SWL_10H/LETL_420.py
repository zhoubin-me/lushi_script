# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_420(SpellEntity):
    """
        苦修5
        对一个敌人造成$12点伤害。随机为一个友方人类恢复#14点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

