# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_083(SpellEntity):
    """
        剧烈爆发
        对本回合中已经行动过的敌人造成10点伤害。在下一场战斗开始时，重复此伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

