# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_024P1(SpellEntity):
    """
        火炮突击5
        <b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，向其发射尤朵拉的火炮。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

