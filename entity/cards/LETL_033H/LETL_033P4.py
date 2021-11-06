# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_033P4(SpellEntity):
    """
        龙喉偷猎者5
        <b>战吼：</b>如果你的对手控制着一条龙，便获得+15/+15和<b>突袭</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

