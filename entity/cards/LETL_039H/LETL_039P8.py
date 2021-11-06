# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_039P8(SpellEntity):
    """
        瞄准射击5
        造成$10点伤害。在本回合中，如果此佣兵未受到伤害，则改为造成$20点伤害。0造成$12点伤害。在本回合中，如果此佣兵未受到伤害，则改为造成$22点伤害。0造成$13点伤害。在本回合中，如果此佣兵未受到伤害，则改为造成$23点伤害。0造成$14点伤害。在本回合中，如果此佣兵未受到伤害，则改为造成$24点伤害。0造成$15点伤害。在本回合中，如果此佣兵未受到伤害，则改为造成$25点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

