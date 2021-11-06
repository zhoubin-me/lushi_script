# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETLT_074p1(SpellEntity):
    """
        巫术之火
        造成$0点伤害。<b>火焰连击：</b>先获得<b>+1火焰伤害</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

