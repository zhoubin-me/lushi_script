# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_253(SpellEntity):
    """
        恶魔印记4
        <b>被动：</b>每当一个友方恶魔攻击时，使其获得+5攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            