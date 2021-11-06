# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_088(SpellEntity):
    """
        烈火突击
        在本回合中提高等同于<b>火焰伤害</b>的攻击力并<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

