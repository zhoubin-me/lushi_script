# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_331(SpellEntity):
    """
        集束暗影5
        造成$10点伤害。如果你拥有驱逐，则改为造成$16点伤害。0造成$11点伤害。如果你拥有驱逐，则改为造成$17点伤害。0造成$12点伤害。如果你拥有驱逐，则改为造成$18点伤害。0造成$13点伤害。如果你拥有驱逐，则改为造成$19点伤害。0造成$14点伤害。如果你拥有驱逐，则改为造成$20点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

