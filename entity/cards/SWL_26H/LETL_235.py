# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_235(SpellEntity):
    """
        末日冲锋5
        <b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（5）点。0<b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（6）点。0<b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（7）点。0<b>攻击</b>一个敌人，并使其下一个技能的速度值减慢（8）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0
        self.is_attack = 1

    def play(self, game, hero, target):
        # 伤害为攻击伤害
        damage = hero.dmg
        # 重新选择攻击目标，因为可能有嘲讽
        target = game.get_attack_target(target)
        target.got_damage(game, damage * self.damage_advantage[self.lettuce_role][target.lettuce_role])
        # 自己受到伤害
        hero.got_damage(game, target.dmg)
