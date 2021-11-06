# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_308(SpellEntity):
    """
        水元素5
        <b>嘲讽</b>。每当此角色造成伤害，<b>冻结</b>受到伤害的角色。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

