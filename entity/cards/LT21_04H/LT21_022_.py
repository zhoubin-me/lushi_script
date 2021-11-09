# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_022_(SpellEntity):
    """
        水手帽4
        重拳猛击使重拳先生额外获得+4攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            