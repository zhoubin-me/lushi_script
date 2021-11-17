# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_006P8(SpellEntity):
    """
        军团爆能5
        造成$14点伤害。<b>击杀：</b>施放加拉克苏斯之拳5。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

