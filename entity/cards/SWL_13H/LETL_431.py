# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_431(SpellEntity):
    """
        制裁之锤5
        对一个角色造成$12点伤害，并使其下一个技能的速度值减慢（3）点。0对一个角色造成$13点伤害，并使其下一个技能的速度值减慢（4）点。0对一个角色造成$14点伤害，并使其下一个技能的速度值减慢（4）点。0对一个角色造成$15点伤害，并使其下一个技能的速度值减慢（5）点。0对一个角色造成$16点伤害，并使其下一个技能的速度值减慢（5）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

