# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_024P3(SpellEntity):
    """
        掩护射击5
        为一个友方佣兵恢复#12点生命值，并将其移回你的后备。发射你的所有火炮。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

