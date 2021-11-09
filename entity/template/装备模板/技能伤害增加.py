# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_700(SpellEntity):
    """
        熔岩之刃4
        热力迸发造成的伤害增加4点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        spell = hero.get_spell_by_cid('LETL_030P3')
        spell.damage += 4
