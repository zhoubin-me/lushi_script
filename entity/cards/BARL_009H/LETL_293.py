# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_293(SpellEntity):
    """
        巨龙符文斧4
        <b>被动：</b>在一条友方的龙<b>攻击</b>一个敌人后，对目标造成10点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            