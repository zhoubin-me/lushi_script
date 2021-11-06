# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_031P7(SpellEntity):
    """
        巨龙吐息5
        对一个敌人造成$14点伤害，或者为一个友方角色恢复#20点生命值。0对一个敌人造成$16点伤害，或者为一个友方角色恢复#22点生命值。0对一个敌人造成$17点伤害，或者为一个友方角色恢复#23点生命值。0对一个敌人造成$18点伤害，或者为一个友方角色恢复#24点生命值。0对一个敌人造成$19点伤害，或者为一个友方角色恢复#25点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

