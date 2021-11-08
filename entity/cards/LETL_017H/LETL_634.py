# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_634(SpellEntity):
    """
        冰风护符4
        <b>亡语：</b>对所有敌人造成$8点伤害。随机<b>冻结</b>一个敌人，直到下回合结束。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            