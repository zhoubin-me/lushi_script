# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_410(SpellEntity):
    """
        部族战争5
        <b>攻击</b>一个敌人。如果你控制着另一个兽人，则先获得+5攻击力。0<b>攻击</b>一个敌人。如果你控制着另一个兽人，则先获得+6攻击力。0<b>攻击</b>一个敌人。如果你控制着另一个兽人，则先获得+7攻击力。0<b>攻击</b>一个敌人。如果你控制着另一个兽人，则先获得+8攻击力。0<b>攻击</b>一个敌人。如果你控制着另一个兽人，则先获得+9攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

