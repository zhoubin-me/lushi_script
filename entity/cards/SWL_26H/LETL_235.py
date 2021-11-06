# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_235(SpellEntity):
    """
        末日冲锋5
        <b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（5）点。0<b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（6）点。0<b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（7）点。0<b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（8）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

