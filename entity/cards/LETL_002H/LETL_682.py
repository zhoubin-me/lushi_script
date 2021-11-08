# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_682(SpellEntity):
    """
        提里奥的护盾4
        <b>被动：</b>+10生命值。对战开始时此佣兵具有<b>圣盾</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            