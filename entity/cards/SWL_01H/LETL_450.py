# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_450(SpellEntity):
    """
        火球术5
        造成$12点伤害。0造成$13点伤害。0造成$14点伤害。0造成$15点伤害。0造成$16点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

