# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_309(SpellEntity):
    """
        战斗怒吼5
        在本回合中，使你的兽人获得+10攻击力。随机<b>攻击</b>一个敌人。0为你的兽人恢复#4点生命值并使其在本回合中获得+10攻击力，随机<b>攻击</b>一个敌人。0为你的兽人恢复#6点生命值并使其在本回合中获得+10攻击力，随机<b>攻击</b>一个敌人。0为你的兽人恢复#8点生命值并使其在本回合中获得+10攻击力，随机<b>攻击</b>一个敌人。0为你的兽人恢复#10点生命值并使其在本回合中获得+10攻击力，随机<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

