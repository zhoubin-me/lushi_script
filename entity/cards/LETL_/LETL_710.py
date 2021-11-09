# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_710(SpellEntity):
    """
        血色匕首4
        <b>被动：</b>每当另一个友方佣兵施放任意<b>连击</b>技能时，获得<b>潜行</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            