# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_338(SpellEntity):
    """
        心灵窃贼5
        此技能始终为随机一个敌方技能的复制，且速度值加快（5）点。<i>（施放后切换。）</i>0此技能始终为上回合中敌方使用的最后一个技能的复制，没有冷却且速度值加快（5）点。<i>（使用后切换。）</i>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

