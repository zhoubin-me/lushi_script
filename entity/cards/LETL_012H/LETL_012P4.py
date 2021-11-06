# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_012P4(SpellEntity):
    """
        反击5
        在本回合中，在一个敌人<b>攻击</b>后，<b>攻击</b>该敌人。0在本回合中，在一个敌人<b>攻击</b>后，获得+1攻击力并<b>攻击</b>该敌人。0在本回合中，在一个敌人<b>攻击</b>后，获得+2攻击力并<b>攻击</b>该敌人。0在本回合中，在一个敌人<b>攻击</b>后，获得+3攻击力并<b>攻击</b>该敌人。0在本回合中，在一个敌人<b>攻击</b>后，获得+4攻击力并<b>攻击</b>该敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

