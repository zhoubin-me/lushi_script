# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_017P6(SpellEntity):
    """
        冰刺5
        对一个角色造成$14点伤害。如果目标已被<b>冻结</b>，则改为造成$24点伤害。0对一个角色造成$16点伤害。如果目标已被<b>冻结</b>，则改为造成$26点伤害。0对一个角色造成$17点伤害。如果目标已被<b>冻结</b>，则改为造成$27点伤害。0对一个角色造成$18点伤害。如果目标已被<b>冻结</b>，则改为造成$28点伤害。0对一个角色造成$19点伤害。如果目标已被<b>冻结</b>，则改为造成$29点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

