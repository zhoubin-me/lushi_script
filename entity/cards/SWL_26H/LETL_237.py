# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_237(SpellEntity):
    """
        末日5
        选择一个敌人，使其在本回合中受到所有身份的角色的<b>爆击伤害</b>。对其造成$12点伤害。0选择一个敌人，使其在本回合中受到所有身份的角色的<b>爆击伤害</b>。对其造成$15点伤害。0选择一个敌人，使其在本回合中受到所有身份的角色的<b>爆击伤害</b>。对其造成$16点伤害。0选择一个敌人，使其在本回合中受到所有身份的角色的<b>爆击伤害</b>。对其造成$17点伤害。0选择一个敌人，使其在本回合中受到所有身份的角色的<b>爆击伤害</b>。对其造成$18点伤害。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 12
        self.range = 1

    def play(self, game, hero, target):
        # 将敌人的角色改成5（受到所有身份的角色的爆击）
        target.lettuce_role = 5
        power = game.get_spell_power(self.spell_school, hero.own)
        target.got_damage(game, (self.damage + power) * self.damage_advantage[self.lettuce_role][target.lettuce_role])
