# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_285(SpellEntity):
    """
        炫彩项链4
        鳞甲嘲讽使此佣兵在本回合中受到的伤害减少3点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            