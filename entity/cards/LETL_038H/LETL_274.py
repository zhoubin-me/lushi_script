# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_274(SpellEntity):
    """
        暴食香蕉5
        <b>攻击</b>一个敌人，使你的角色随机获得5根香蕉。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

