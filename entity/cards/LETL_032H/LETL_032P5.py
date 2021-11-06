# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_032P5(SpellEntity):
    """
        相位变换5
        为此佣兵恢复#25点生命值，并将其与后备中生命值最高的佣兵交换。0为此佣兵恢复#35点生命值，并将其与后备中生命值最高的佣兵交换。0为此佣兵恢复#40点生命值，并将其与后备中生命值最高的佣兵交换。0为此佣兵恢复#45点生命值，并将其与后备中生命值最高的佣兵交换。0为此佣兵恢复#50点生命值，并将其与后备中生命值最高的佣兵交换。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

