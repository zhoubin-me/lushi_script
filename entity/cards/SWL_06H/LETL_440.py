# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_440(SpellEntity):
    """
        武艺精通5
        获得+5生命值并<b>攻击</b>一个敌人。如果目标为斗士，改为获得+10生命值。0获得+6生命值并<b>攻击</b>一个敌人。如果目标为斗士，改为获得+11生命值。0获得+7生命值并<b>攻击</b>一个敌人。如果目标为斗士，改为获得+12生命值。0获得+8生命值并<b>攻击</b>一个敌人。如果目标为斗士，改为获得+13生命值。0获得+9生命值并<b>攻击</b>一个敌人。如果目标为斗士，改为获得+14生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

