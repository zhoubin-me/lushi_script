# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_330(SpellEntity):
    """
        集束之光5
        恢复#10点生命值。如果你拥有祈福，则改为恢复#20点生命值。0恢复#12点生命值。如果你拥有祈福，则改为恢复#22点生命值。0恢复#14点生命值。如果你拥有祈福，则改为恢复#24点生命值。0恢复#16点生命值。如果你拥有祈福，则改为恢复#26点生命值。0恢复#18点生命值。如果你拥有祈福，则改为恢复#28点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

