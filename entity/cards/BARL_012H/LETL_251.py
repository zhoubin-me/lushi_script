# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_251(SpellEntity):
    """
        恐惧嚎叫5
        在本回合中，使所有敌人的攻击力降低15点。0在本回合中，使所有敌人的攻击力降低15点。对所有敌人造成2点伤害。0在本回合中，使所有敌人的攻击力降低15点。对所有敌人造成3点伤害。0在本回合中，使所有敌人的攻击力降低15点。对所有敌人造成4点伤害。0在本回合中，使所有敌人的攻击力降低15点。对所有敌人造成5点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

