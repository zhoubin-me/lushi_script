# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_054(SpellEntity):
    """
        飞掠攻击
        <b>攻击</b>一个敌人，攻击时具有<b>免疫</b>。然后使你的所有角色获得+2攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

