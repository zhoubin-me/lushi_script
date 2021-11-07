# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_256(SpellEntity):
    """
        闪电军团5
        <b>攻击</b>一个敌人。如果你控制着另一个恶魔，则随机对一个敌人造成$7点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

