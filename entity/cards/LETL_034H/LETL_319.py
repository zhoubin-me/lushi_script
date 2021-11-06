# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_319(SpellEntity):
    """
        坚韧光环5
        获得<b>嘲讽</b>2回合。在本回合中，你的角色的速度值加快（4）点。0获得<b>嘲讽</b>2回合。在本回合中，你的角色的速度值加快（4）点。此佣兵的下一个技能速度值加快（1）点。0获得<b>嘲讽</b>2回合。在本回合中，你的角色的速度值加快（4）点。此佣兵的下一个技能速度值加快（2）点。0获得<b>嘲讽</b>2回合。在本回合中，你的角色的速度值加快（4）点。此佣兵的下一个技能速度值加快（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

