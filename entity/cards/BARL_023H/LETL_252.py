# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_252(SpellEntity):
    """
        巨型大恶魔5
        <b>突袭</b>。<b>击杀：</b><b>攻击</b>生命值最低的敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

