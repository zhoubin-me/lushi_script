# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_020P6(SpellEntity):
    """
        光明圣印5
        选择一个角色，使其获得+6攻击力并为其恢复#15点生命值。0选择一个角色，使其获得+7攻击力并为其恢复#15点生命值。0选择一个角色，使其获得+8攻击力并为其恢复#15点生命值。0选择一个角色，使其获得+9攻击力并为其恢复#15点生命值。0选择一个角色，使其获得+10攻击力并为其恢复#15点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

