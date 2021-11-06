# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_716(SpellEntity):
    """
        纳鲁碎片4
        快速治疗恢复的生命值增加20点，但具有（1）冷却。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            