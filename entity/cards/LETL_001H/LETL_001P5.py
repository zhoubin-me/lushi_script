# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_001P5(SpellEntity):
    """
        重拾灵魂5
        在本局对战中，每有一个友方角色死亡，便获得+5攻击力。0在本局对战中，每有一个友方角色死亡，便获得+6攻击力。0在本局对战中，每有一个友方角色死亡，便获得+7攻击力。0在本局对战中，每有一个友方角色死亡，便获得+8攻击力。0在本局对战中，每有一个友方角色死亡，便获得+9攻击力。
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 0

    def play(self, game, hero, target):
        pass

