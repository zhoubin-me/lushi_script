# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_657(SpellEntity):
    """
        埃提耶什4
        <b>被动：</b>在此佣兵受到伤害后，召唤一只6/6并具有<b>突袭</b>的乌鸦。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            