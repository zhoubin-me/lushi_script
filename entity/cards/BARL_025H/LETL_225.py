# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_225(SpellEntity):
    """
        大酋长的命令5
        对一个敌人造成$12点伤害，并使你最左边的角色<b>攻击</b>它。0对一个敌人造成$14点伤害，并使你最左边的角色<b>攻击</b>它。0对一个敌人造成$15点伤害，并使你最左边的角色<b>攻击</b>它。0对一个敌人造成$16点伤害，并使你最左边的角色<b>攻击</b>它。0对一个敌人造成$17点伤害，并使你最左边的角色<b>攻击</b>它。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

