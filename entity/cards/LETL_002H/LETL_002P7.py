# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_002P7(SpellEntity):
    """
        神圣突击5
        <b>攻击</b>一个敌人。<b>击杀：</b>使你的角色获得<b>圣盾</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

