# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_715(SpellEntity):
    """
        强光魔杖4
        致盲之光造成的伤害增加4点，且使目标额外获得-4攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            