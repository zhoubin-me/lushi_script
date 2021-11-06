# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_039P6(SpellEntity):
    """
        捕熊陷阱5
        在本回合中，此佣兵第一次受到伤害时，召唤一只15/20并具有<b>嘲讽</b>的野兽。0在本回合中，此佣兵第一次受到伤害时，召唤一只17/20并具有<b>突袭</b>和<b>嘲讽</b>的野兽。0在本回合中，此佣兵第一次受到伤害时，召唤一只18/20并具有<b>突袭</b>和<b>嘲讽</b>的野兽。0在本回合中，此佣兵第一次受到伤害时，召唤一只19/20并具有<b>突袭</b>和<b>嘲讽</b>的野兽。0在本回合中，此佣兵第一次受到伤害时，召唤一只20/20并具有<b>突袭</b>和<b>嘲讽</b>的野兽。0此佣兵第一次受到伤害时，召唤一只15/20并具有<b>嘲讽</b>的野兽。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

