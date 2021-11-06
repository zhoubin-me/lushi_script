# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_057(SpellEntity):
    """
        粉碎冰旋
        在本回合中提高等同于<b>冰霜伤害</b>的攻击力。<b>攻击</b>两个不同的敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

