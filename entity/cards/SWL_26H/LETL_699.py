# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_699(SpellEntity):
    """
        恐怖利爪4
        <b>被动：</b>+5攻击力。末日冲锋会使敌人的速度值额外减慢（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            