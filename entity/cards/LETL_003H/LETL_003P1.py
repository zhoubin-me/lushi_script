# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_003P1(SpellEntity):
    """
        流放攻击5
        <b>攻击</b>最左边和最右边的敌人。<b>击杀：</b>为此佣兵恢复#25点生命值。0<b>攻击</b>最左边的敌人两次，最右边的敌人一次。<b>击杀：</b>为此佣兵恢复#25点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

