# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_258(SpellEntity):
    """
        邪能命令5
        获得+5攻击力。对一个敌人造成等同于此佣兵攻击力的伤害。0获得+5/+4。对一个敌人造成等同于此佣兵攻击力的伤害。0获得+5/+6。对一个敌人造成等同于此佣兵攻击力的伤害。0获得+5/+8。对一个敌人造成等同于此佣兵攻击力的伤害。0获得+5/+10。对一个敌人造成等同于此佣兵攻击力的伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

