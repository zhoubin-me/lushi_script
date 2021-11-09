# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_455(SpellEntity):
    """
        烈焰饰环4
        烈焰风暴造成的伤害增加5点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        spell = hero.get_spell_by_cid('LETL_451')
        spell.damage += 5

            