# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_017P7(SpellEntity):
    """
        冰枪术5
        在本回合中<b>冻结</b>一个角色。如果目标已被<b>冻结</b>，则改为造成$25点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

