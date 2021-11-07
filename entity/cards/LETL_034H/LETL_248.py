# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_248(SpellEntity):
    """
        雷霆饰带4
        大地践踏造成的伤害增加5点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        spell = hero.get_spell_by_cid('LETL_246')
        spell.damage += 5

            