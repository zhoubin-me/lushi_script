# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_003(SpellEntity):
    """
        辅助打击5
        每有一个友方海盗便获得+{0}攻击力，并随机<b>攻击</b>一个敌人。<b>连击：</b>在本回合<b>攻击</b>时获得<b>免疫</b>。5每有一个友方海盗便获得+{0}攻击力。在本回合<b>攻击</b>时获得<b>免疫</b>，并随机<b>攻击</b>一个敌人。5每有一个友方海盗便获得+{0}攻击力。在本回合<b>攻击</b>时获得<b>免疫</b>，并随机<b>攻击</b>一个敌人。5每有一个友方海盗便获得+{0}攻击力。在本回合<b>攻击</b>时获得<b>免疫</b>，并随机<b>攻击</b>一个敌人。5每有一个友方海盗便获得+{0}攻击力。在本回合<b>攻击</b>时获得<b>免疫</b>，并随机<b>攻击</b>一个敌人。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

