# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_337(SpellEntity):
    """
        法力闪现5
        刷新你的角色的技能，并使其下一个技能的速度值加快（5）点。0<b>刷新</b>你的角色的技能，并使其下一个技能的速度值加快（6）点。0<b>刷新</b>你的角色的技能，并使其下一个技能的速度值加快（7）点。0<b>刷新</b>你的角色的技能，并使其下一个技能的速度值加快（8）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

