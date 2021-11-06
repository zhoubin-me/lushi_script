# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_404(SpellEntity):
    """
        奥术齐射5
        随机对两个敌人造成$8点伤害。0随机对两个敌人造成$9点伤害。0随机对两个敌人造成$10点伤害。0随机对两个敌人造成$11点伤害。0随机对两个敌人造成$12点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

