# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_324(SpellEntity):
    """
        暗影涌动5
        对所有敌人造成$10点伤害。<b>暗影连击</b>：改为造成$16点伤害。0对所有敌人造成$11点伤害。<b>暗影连击</b>：改为造成$17点伤害。0对所有敌人造成$12点伤害。<b>暗影连击</b>：改为造成$18点伤害。0对所有敌人造成$13点伤害。<b>暗影连击</b>：改为造成$19点伤害。0对所有敌人造成$14点伤害。<b>暗影连击</b>：改为造成$20点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

