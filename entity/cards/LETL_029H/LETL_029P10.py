# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_029P10(SpellEntity):
    """
        陷足泥泞5
        对一个角色造成$10点伤害，并使其下一个技能速度值减慢（6）点。0对一个角色造成$10点伤害，并使其下一个技能速度值减慢（7）点。0对一个角色造成$10点伤害，并使其下一个技能速度值减慢（8）点。0对一个角色造成$10点伤害，并使其下一个技能速度值减慢（9）点。0对一个角色造成$10点伤害，并使其下一个技能速度值减慢（10）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

