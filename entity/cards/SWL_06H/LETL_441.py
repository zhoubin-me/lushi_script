# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_441(SpellEntity):
    """
        坚守前线5
        获得<b>嘲讽</b>2回合。为相邻的角色恢复#14点生命值。0获得<b>嘲讽</b>2回合。为相邻的角色恢复#16点生命值。0获得<b>嘲讽</b>2回合。为相邻的角色恢复#18点生命值。0获得<b>嘲讽</b>2回合。为相邻的角色恢复#20点生命值。0获得<b>嘲讽</b>2回合。为相邻的角色恢复#22点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

