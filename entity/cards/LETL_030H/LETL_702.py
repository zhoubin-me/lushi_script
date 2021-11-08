# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_702(SpellEntity):
    """
        燃烧护腕4
        活体炸弹造成伤害两次，但具有+1冷却。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):

        spell = hero.get_spell_by_cid('LETL_030P6')

        spell.trigger_twice = 1

            