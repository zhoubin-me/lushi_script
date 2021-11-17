# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_024_(SpellEntity):
    """
        沉重铁锚4
        如果受伤的友方角色是海盗，则落水追击获得+6攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            