# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_040(SpellEntity):
    """
        熊怪的防御
        <b>攻击</b>一个敌人。如果目标已经行动，则使你的角色获得+0攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

