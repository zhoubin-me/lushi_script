# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_224(SpellEntity):
    """
        部落之力5
        获得<b>嘲讽</b>，持续2回合。每有一个敌方角色，便获得+10生命值。0获得<b>嘲讽</b>，持续2回合。每有一个敌方角色，便获得+12生命值。0获得<b>嘲讽</b>，持续2回合。每有一个敌方角色，便获得+14生命值。0获得<b>嘲讽</b>，持续2回合。每有一个敌方角色，便获得+16生命值。0获得<b>嘲讽</b>，持续2回合。每有一个敌方角色，便获得+18生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

