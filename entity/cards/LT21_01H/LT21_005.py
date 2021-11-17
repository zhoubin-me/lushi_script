# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_005(SpellEntity):
    """
        公平分配4
        首脑的悬赏额外恢复10点生命值，并会影响所有友方角色。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            