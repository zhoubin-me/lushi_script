# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_306(SpellEntity):
    """
        冰风暴5
        随机对3个敌方佣兵造成$6点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$7点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$8点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$9点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$10点伤害，并使其下回合的速度值减慢（2）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

