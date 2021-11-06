# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_040P7(SpellEntity):
    """
        虚空吞噬者5
        <b>嘲讽</b>。在你施放一个暗影技能后，获得+3/+5。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

