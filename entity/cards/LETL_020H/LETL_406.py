# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_406(SpellEntity):
    """
        远征军打击5
        <b>攻击</b>一个敌人。<b>击杀：</b>为此佣兵恢复#40点生命值。0<b>攻击</b>一个敌人。<b>击杀：</b>为你的队伍恢复#40点生命值。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

