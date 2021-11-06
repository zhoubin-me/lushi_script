# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_282(SpellEntity):
    """
        顶级捕食者5
        <b>攻击</b>生命值最低的敌人。<b>击杀：</b>重复此效果。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = -1

    def play(self, game, hero, target):
        # 伤害为攻击伤害
        damage = hero.dmg
        # 攻击生命最低
        while True:
            h = game.find_min_health(not hero.own())
            if h is None:
                break
            h.got_damage(game, damage * self.damage_advantage[self.lettuce_role][h.lettuce_role])
            # 自己受到伤害
            hero.got_damage(game, h.dmg)
            if not h.is_alive():
                break
