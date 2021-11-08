# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_007P8(SpellEntity):
    """
        恶魔卫士4
        <b>被动：</b>+4攻击力。此佣兵始终对恶魔造成<b>爆击伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            