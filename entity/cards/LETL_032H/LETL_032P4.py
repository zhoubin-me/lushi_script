# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_032P4(SpellEntity):
    """
        妖精之尘5
        为你的所有角色恢复#18点生命值。0为你的所有角色恢复#20点生命值。0为你的所有角色恢复#22点生命值。0为你的所有角色恢复#24点生命值。0为你的所有角色恢复#26点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

