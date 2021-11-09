# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_306(SpellEntity):
    """
        冰风暴5
        随机对3个敌方佣兵造成$6点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$7点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$8点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$9点伤害，并使其下回合的速度值减慢（2）点。0随机对3个敌方佣兵造成$10点伤害，并使其下回合的速度值减慢（2）点。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 6
        self.range = 3

    def play(self, game, hero, target):
        power = game.get_spell_power(self.spell_school, hero.own)
        hero_list = game.get_hero_list(not hero.own())
        for i, h in enumerate(hero_list):
            if i >= 3:
                break
            h.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][
                h.lettuce_role])
