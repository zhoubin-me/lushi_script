# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_002P4(SpellEntity):
    """
        王者祝福5
        使一个角色获得+8/+8和<b>圣盾</b>。0使一个角色获得+8/+8和<b>圣盾</b>。使此佣兵获得+1/+1。0使一个角色获得+8/+8和<b>圣盾</b>。使此佣兵获得+2/+2。0使一个角色获得+8/+8和<b>圣盾</b>。使此佣兵获得+3/+3。0使一个角色获得+8/+8和<b>圣盾</b>。使此佣兵获得+4/+4。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

