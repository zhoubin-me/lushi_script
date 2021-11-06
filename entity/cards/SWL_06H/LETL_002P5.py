# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_002P5(SpellEntity):
    """
        牺牲祝福5
        为另一名友方佣兵恢复#10点生命值。在本回合中，每当其受到伤害时，改为由此佣兵来承担。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

