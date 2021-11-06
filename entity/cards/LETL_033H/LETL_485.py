# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_485(SpellEntity):
    """
        巨龙之颅4
        <b>被动：</b>你的角色具有<b>+5火焰抗性。</b>
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            