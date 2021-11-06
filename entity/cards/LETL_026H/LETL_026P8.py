# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_026P8(SpellEntity):
    """
        鱼人入侵5
        <b>攻击</b>一个敌人，并使你的其他鱼人<b>攻击</b>目标。0获得+2攻击力和<b>圣盾</b>，<b>攻击</b>一个敌人，并使你的其他鱼人<b>攻击</b>目标。0获得+3攻击力和<b>圣盾</b>，<b>攻击</b>一个敌人，并使你的其他鱼人<b>攻击</b>目标。0获得+4攻击力和<b>圣盾</b>，<b>攻击</b>一个敌人，并使你的其他鱼人<b>攻击</b>目标。0获得+5攻击力和<b>圣盾</b>，<b>攻击</b>一个敌人，并使你的其他鱼人<b>攻击</b>目标。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

