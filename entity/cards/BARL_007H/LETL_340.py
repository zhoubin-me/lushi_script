# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_340(SpellEntity):
    """
        毒蛇噬咬5
        对一个角色造成$6点伤害。在本回合结束时，使其受到$6点伤害。0对一个角色造成$7点伤害。在本回合结束时，使其受到$7点伤害。0对一个角色造成$8点伤害。在本回合结束时，使其受到$8点伤害。0对一个角色造成$9点伤害。在本回合结束时，使其受到$9点伤害。0对一个角色造成$10点伤害。在本回合结束时，使其受到$10点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0

    def play(self, hero, target):
        pass

