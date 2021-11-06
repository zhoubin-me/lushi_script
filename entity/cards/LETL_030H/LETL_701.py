# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_701(SpellEntity):
    """
        焚火印记
        地狱火的火焰连击造成的伤害增加5点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        spell = hero.get_spell_by_cid('LETL_030P4')
        spell.combo_damage += 5
