# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_022P7(SpellEntity):
    """
        奥术裂隙3
        对一个敌人造成$20点伤害。<b>击杀：</b><b>复原</b>此技能。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

