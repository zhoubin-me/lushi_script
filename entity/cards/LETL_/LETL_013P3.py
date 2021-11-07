# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_013P3(SpellEntity):
    """
        刀扇5
        对所有敌人造成$10点伤害。下回合你的其他佣兵速度值加快（3）点。0对所有敌人造成$10点伤害。下回合你的其他佣兵速度值加快（4）点。0对所有敌人造成$10点伤害。下回合你的其他佣兵速度值加快（5）点。0对所有敌人造成$10点伤害。下回合你的其他佣兵速度值加快（6）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

