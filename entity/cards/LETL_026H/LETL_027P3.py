# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_027P3(SpellEntity):
    """
        邪鳍导航员5
        <b>战吼：</b>使你的其他鱼人获得+3/+5。0<b>战吼：</b>使你的其他鱼人获得+5/+7。0<b>战吼：</b>使你的其他鱼人获得+6/+8。0<b>战吼：</b>使你的其他鱼人获得+7/+9。0<b>战吼：</b>使你的其他鱼人获得+8/+10。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

