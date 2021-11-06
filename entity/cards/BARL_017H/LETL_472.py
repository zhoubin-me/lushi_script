# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_472(SpellEntity):
    """
        大德鲁伊的召唤5
        <b>抉择：</b>对所有敌人造成$12点伤害；或者为你的角色恢复#24点生命值。0<b>抉择：</b>对所有敌人造成$14点伤害；或者为你的角色恢复#24点生命值。0<b>抉择：</b>对所有敌人造成$15点伤害；或者为你的角色恢复#24点生命值。0<b>抉择：</b>对所有敌人造成$16点伤害；或者为你的角色恢复#24点生命值。0<b>抉择：</b>对所有敌人造成$17点伤害；或者为你的角色恢复#24点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

