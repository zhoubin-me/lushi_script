# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_029P12(SpellEntity):
    """
        治疗波5
        恢复#15点生命值。如果目标尚未行动，则改为恢复#30点生命值。0恢复#19点生命值。如果目标尚未行动，则改为恢复#34点生命值。0恢复#21点生命值。如果目标尚未行动，则改为恢复#36点生命值。0恢复#23点生命值。如果目标尚未行动，则改为恢复#38点生命值。0恢复#25点生命值。如果目标尚未行动，则改为恢复#40点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

