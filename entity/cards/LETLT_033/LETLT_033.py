# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_033(SpellEntity):
    """
        双生
        <b>攻击</b>一个敌人。如果此角色没有死亡，召唤一个此角色的复制。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

