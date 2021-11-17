# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_423(SpellEntity):
    """
        纯洁指环4
        <b>被动：</b>每当一个友方角色被治疗时，使其获得+5生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            