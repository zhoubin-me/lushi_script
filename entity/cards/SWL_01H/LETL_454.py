# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_454(SpellEntity):
    """
        灼热吊坠4
        火球风暴会随机对两个敌人施放火球术，但冷却+1。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        spell = hero.get_spell_by_cid('LETL_452')

        spell.trigger_twice = 1

            