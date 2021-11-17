# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_411(SpellEntity):
    """
        进攻集结5
        在本回合中，每当一个友方角色<b>攻击</b>时，使其获得+5/+10。0在本回合中，每当一个友方角色<b>攻击</b>时，使其获得+6/+12。0在本回合中，每当一个友方角色<b>攻击</b>时，使其获得+6/+13。0在本回合中，每当一个友方角色<b>攻击</b>时，使其获得+7/+13。0在本回合中，每当一个友方角色<b>攻击</b>时，使其获得+7/+14。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

