# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_685(SpellEntity):
    """
        圣光秘典4
        <b>被动：</b>当此佣兵具有<b>嘲讽</b>时，具有+8攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            