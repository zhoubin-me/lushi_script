# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_059(SpellEntity):
    """
        先行屠灭
        获得<b>嘲讽</b>。如果此角色已经具有<b>嘲讽</b>，则对所有敌人造成$5点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

