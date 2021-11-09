# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_034P3(SpellEntity):
    """
        先祖勾拳5
        <b>攻击</b>一个敌人。每有一个尚未行动的敌人，便恢复#8点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.heal = 8
        self.range = 1
        self.is_attack = 1

    def play(self, game, hero, target):
        # 伤害为攻击伤害
        damage = hero.dmg

        # 获取技能列表
        action_list = game.get_action_list(not hero.own)
        action_list.sort()
        # self.cost 这个技能的速度,
        cnt = 0
        for action in action_list:
            if action.spell.cost >= self.cost:
                # 假设同速下，我方先使用技能
                cnt += 1
        # 攻击
        # 重新选择攻击目标，因为可能有嘲讽
        target = game.get_attack_target(target)
        target.got_damage(game, damage * self.damage_advantage[self.lettuce_role][target.lettuce_role])
        # 自己受到伤害
        hero.got_damage(game, target.dmg)
        # 回复
        hero.got_heal(game, cnt * self.heal)
