# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_481(SpellEntity):
    """
        暗影之刃5
        <b>攻击</b>一个敌人，然后获得<b>潜行</b>。0获得+1攻击力，<b>攻击</b>一个敌人，然后获得<b>潜行</b>。0获得+2攻击力，<b>攻击</b>一个敌人，然后获得<b>潜行</b>。0获得+3攻击力，<b>攻击</b>一个敌人，然后获得<b>潜行</b>。0获得+4攻击力，<b>攻击</b>一个敌人，然后获得<b>潜行</b>。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

