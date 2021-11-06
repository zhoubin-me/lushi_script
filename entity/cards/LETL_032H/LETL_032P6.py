# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_032P6(SpellEntity):
    """
        精灵吐息5
        造成$10点伤害。随机使你后备中的一名友方佣兵获得+3/+5。0造成$10点伤害。随机使你后备中的一名友方佣兵获得+3/+7。0造成$10点伤害。随机使你后备中的一名友方佣兵获得+3/+8。0造成$10点伤害。随机使你后备中的一名友方佣兵获得+3/+9。0造成$10点伤害。随机使你后备中的一名友方佣兵获得+3/+10。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

