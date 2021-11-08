# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_654(SpellEntity):
    """
        魔网之杖4
        强能奥术飞弹总是会以生命值最低的敌人为目标。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            