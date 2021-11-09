# -*- coding: utf-8 -*-
from hearthstone.entities import Entity
from hearthstone.enums import SpellSchool

from entity.spell_entity import SpellEntity


class LETL_028P11(SpellEntity):
    """
        熔岩冲击5
        造成$10点伤害。<b>火焰连击：</b>改为造成$18点伤害。0造成$12点伤害。<b>火焰连击：</b>改为造成$20点伤害。0造成$13点伤害。<b>火焰连击：</b>改为造成$21点伤害。0造成$14点伤害。<b>火焰连击：</b>改为造成$22点伤害。0造成$15点伤害。<b>火焰连击：</b>改为造成$23点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 10
        self.combo_damage = 18
        self.range = 1

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        # 获取技能列表
        action_list = game.get_action_list(hero.own)
        action_list.sort()
        combo = game.can_combo(self, SpellSchool.FIRE, hero.own)
        damage = self.combo_damage if combo else self.damage
        target.got_damage(game, (damage + power) * self.damage_advantage[self.lettuce_role][target.lettuce_role])
