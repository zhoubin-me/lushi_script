# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_048(SpellEntity):
    """
        裂伤
        <b>攻击</b>一个敌人。直到目标被治疗，造成的伤害会在每个回合结束时重复。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

