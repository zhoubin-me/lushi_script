# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_433(SpellEntity):
    """
        光明使者4
        制裁之锤造成的伤害增加4点，并使目标的速度值额外减慢（2）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            