# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_071p1(SpellEntity):
    """
        充能打击
        <b>攻击</b>一个敌人。其他友方龙的下一个技能速度值加快（0）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

