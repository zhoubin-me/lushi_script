# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_480(SpellEntity):
    """
        邪恶挥刺5
        可选择造成$10，$15或$20点伤害。<i>（施放的速度值不同。）</i>0可选择造成$12，$17或$22点伤害。<i>（施放的速度值不同。）</i>0可选择造成$13，$18或$23点伤害。<i>（施放的速度值不同。）</i>0可选择造成$14，$19或$24点伤害。<i>（施放的速度值不同。）</i>0可选择造成$15，$20或$25点伤害。<i>（施放的速度值不同。）</i>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

