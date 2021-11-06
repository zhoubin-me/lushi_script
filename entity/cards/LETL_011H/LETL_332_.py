# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_332_(SpellEntity):
    """
        咒逐5
        对所有敌人造成$14点伤害。<i>（变形成为祈福）</i>0对所有敌人造成$15点伤害。<i>（变形成为祈福）</i>0对所有敌人造成$16点伤害。<i>（变形成为祈福）</i>0对所有敌人造成$17点伤害。<i>（变形成为祈福）</i>0对所有敌人造成$18点伤害。<i>（变形成为祈福）</i>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

