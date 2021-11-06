# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_060(SpellEntity):
    """
        刺骨之寒
        <b>攻击</b>一个敌人，并对其相邻敌人造成$3点伤害。<b>冻结</b>其中在本回合中未使用过火焰技能的敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

