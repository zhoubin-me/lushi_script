# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_611(SpellEntity):
    """
        巨龙军团护身符4
        红龙女王的计策会为此佣兵恢复等同于所造成伤害的生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            