from typing import Dict

from hearthstone.entities import Entity
from hearthstone.enums import GameTag, Zone

from .base_entity import BaseEntity
from .hero_entity import HeroEntity


class GameEntity(BaseEntity):

    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.players = []
        # 所有英雄
        self.hero_entities: Dict[int, HeroEntity] = {}
        # 我方场上
        self.my_hero: Dict[int, HeroEntity] = {}
        # 敌方场上
        self.enemy_hero: Dict[int, HeroEntity] = {}
        # 手牌上
        self.setaside_hero: Dict[int, HeroEntity] = {}
        # 1为选择随从 0为战斗
        self.action_step_type = 1
        self.turn = 0  # 回合数
        # 允许移动随从
        self.allow_move_minion = 0
        self.parse_entity()

    def parse_entity(self):
        if self.entity is None:
            return
        super(GameEntity, self).parse_entity()
        self.players = self.entity.players
        self.action_step_type = self.get_tag(GameTag.ACTION_STEP_TYPE)
        self.turn = self.get_tag(GameTag.TURN)
        self.allow_move_minion = self.get_tag(GameTag.ALLOW_MOVE_MINION)

        pass

    def add_hero(self, hero: HeroEntity):
        self.hero_entities[hero.entity_id] = hero
        if hero.zone == Zone.PLAY:
            if hero.own():
                self.my_hero[hero.entity_id] = hero
            else:
                self.enemy_hero[hero.entity_id] = hero
        elif hero.zone == Zone.SETASIDE:
            self.setaside_hero[hero.entity_id] = hero
