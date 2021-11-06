# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_408(SpellEntity):
    """
        救赎5
        造成${0}点伤害。你每恢复20点生命值，伤害+3。<i>（还剩{1}点。）</i>15造成${0}点伤害。你每恢复18点生命值，伤害+3。<i>（还剩{1}点。）</i>15造成${0}点伤害。你每恢复17点生命值，伤害+3。<i>（还剩{1}点。）</i>15造成${0}点伤害。你每恢复16点生命值，伤害+3。<i>（还剩{1}点。）</i>15造成${0}点伤害。你每恢复15点生命值，伤害+3。<i>（还剩{1}点。）</i>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

