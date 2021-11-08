# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_658(SpellEntity):
    """
        阿莱克丝塔萨的胸针4
        巨龙吐息造成的伤害或恢复的生命值增加5点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            