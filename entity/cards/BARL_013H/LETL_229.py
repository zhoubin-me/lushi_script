# -*- coding: utf-8 -*-
from hearthstone.entities import Entity

from entity.spell_entity import SpellEntity


class LETL_229(SpellEntity):
    """
        荣耀决斗5
        <b>攻击</b>一个敌人，并使其<b>攻击</b>此佣兵。0<b>攻击</b>一个敌人，并使其<b>攻击</b>此佣兵。如果此佣兵的生命值少于或等于20点，则战斗至死！0<b>攻击</b>一个敌人，并使其<b>攻击</b>此佣兵。如果此佣兵的生命值少于或等于30点，则战斗至死！0<b>攻击</b>一个敌人，并使其<b>攻击</b>此佣兵。如果此佣兵的生命值少于或等于40点，则战斗至死！0<b>攻击</b>一个敌人，并使其<b>攻击</b>此佣兵。如果此佣兵的生命值少于或等于50点，则战斗至死！
    """

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.damage = 0
        self.range = 1

    def play(self, hero, target):
        pass

