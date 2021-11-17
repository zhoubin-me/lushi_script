# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_375(SpellEntity):
    """
        狂野的徽记4
        野兽恢复也会为安娜科德拉恢复生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            