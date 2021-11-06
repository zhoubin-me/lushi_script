# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_009P7(SpellEntity):
    """
        热血5
        <b>攻击</b>一个敌人。<b>击杀：</b>获得+15攻击力。0<b>攻击</b>一个敌人。<b>击杀：</b>获得+15攻击力并恢复#5点生命值。0<b>攻击</b>一个敌人。<b>击杀：</b>获得+15攻击力并恢复#10点生命值。0<b>攻击</b>一个敌人。<b>击杀：</b>获得+15攻击力并恢复#15点生命值。0<b>攻击</b>一个敌人。<b>击杀：</b>获得+15攻击力并恢复#20点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

