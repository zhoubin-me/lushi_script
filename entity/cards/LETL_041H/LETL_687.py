# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_687(SpellEntity):
    """
        统御头盔4
        <b>被动：</b>在一个敌人施放速度值大于或等于（7）点的技能后，对其造成10点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            