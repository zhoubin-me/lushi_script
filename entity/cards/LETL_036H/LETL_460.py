# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_460(SpellEntity):
    """
        符文猛击5
        <b>攻击</b>一个敌人。<b>击杀：</b>使你场上和后备的所有佣兵获得+3/+10。0<b>攻击</b>一个敌人。<b>击杀：</b>使你场上和后备的所有佣兵获得+4/+13。0<b>攻击</b>一个敌人。<b>击杀：</b>使你场上和后备的所有佣兵获得+4/+14。0<b>攻击</b>一个敌人。<b>击杀：</b>使你场上和后备的所有佣兵获得+5/+14。0<b>攻击</b>一个敌人。<b>击杀：</b>使你场上和后备的所有佣兵获得+5/+15。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

