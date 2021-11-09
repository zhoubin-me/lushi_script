# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_326(SpellEntity):
    """
        急速指环4
        <b>被动：</b>你的暗影技能的速度值加快（3）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            