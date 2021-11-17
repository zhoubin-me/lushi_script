# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_032(SpellEntity):
    """
        暗影鞭笞
        <b>攻击</b>一个敌人。如果目标尚未行动，则召唤一个伊利达雷萨特。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

