# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_698(SpellEntity):
    """
        第十条尾巴4
        心灵窃贼总是会偷取上个回合敌方使用的最后一个技能，且没有冷却。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)

    def equip(self, hero):
        pass

            