# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LT21_015_(SpellEntity):
    """
        滋啦5
        造成等同于你攻击力的伤害。如果启动电锯效果激活，则同时对目标相邻的角色造成伤害。0造成等同于你攻击力的伤害。如果启动电锯效果激活，则同时对目标相邻的角色造成伤害。<b>流血（2）</b>。0造成等同于你攻击力的伤害。如果启动电锯效果激活，则同时对目标相邻的角色造成伤害。<b>流血（3）</b>。0造成等同于你攻击力的伤害。如果启动电锯效果激活，则同时对目标相邻的角色造成伤害。<b>流血（4）</b>。0造成等同于你攻击力的伤害。如果启动电锯效果激活，则同时对目标相邻的角色造成伤害。<b>流血（5）</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, game, hero, target):
        pass

