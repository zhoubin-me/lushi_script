# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_670(SpellEntity):
    """
        霜冻之戒4
        <b>被动：</b>在你<b>冻结</b>一个敌人后，获得<b>+3冰霜伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            