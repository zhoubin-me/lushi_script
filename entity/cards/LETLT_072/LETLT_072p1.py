# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_072p1(SpellEntity):
    """
        喂食时间
        <b>攻击</b>生命值最低的敌人。<b>击杀：</b>恢复0点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

