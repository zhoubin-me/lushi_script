# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_003P8(SpellEntity):
    """
        侧翼突击5
        <b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，便获得+5攻击力。0<b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，便获得+7攻击力。0<b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，便获得+8攻击力。0<b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，便获得+9攻击力。0<b>攻击</b>一个敌人。如果目标为最左边或最右边的敌人，便获得+10攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

