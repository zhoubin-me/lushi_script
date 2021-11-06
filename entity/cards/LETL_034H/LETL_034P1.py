# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_034P1(SpellEntity):
    """
        重生4
        <b>被动：</b>此佣兵第一次死亡时，将其复活并具有40点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            