# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_012P7(SpellEntity):
    """
        爆裂打击5
        <b>攻击</b>一个敌人。<b>击杀：</b>使你的人类获得+12攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

