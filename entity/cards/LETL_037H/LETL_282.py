# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_282(SpellEntity):
    """
        顶级捕食者5
        <b>攻击</b>生命值最低的敌人。<b>击杀：</b>重复此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

