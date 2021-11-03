from typing import Dict, List

from hearthstone.entities import Entity
from hearthstone.enums import GameTag, Zone, SpellSchool

from .base_entity import BaseEntity
from .hero_entity import HeroEntity
from .spell_entity import SpellEntity


class GameEntity(BaseEntity):

    def __init__(self, entity: Entity):
        super().__init__(entity)
        # 所有英雄
        self.hero_entities: Dict[int, HeroEntity] = {}
        # 我方场上0, 1, 2号随从(只有战斗阶段才有数据)
        self.my_hero: List[HeroEntity] = []
        # 敌方场上0, 1, 2
        self.enemy_hero: List[HeroEntity] = []
        # 手牌上(从左往右按顺序)
        self.setaside_hero: List[HeroEntity] = []
        # 死掉的
        self.dead_hero: List[HeroEntity] = []
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
        self.action_step_type = self.get_tag(GameTag.ACTION_STEP_TYPE)
        self.turn = self.get_tag(GameTag.TURN)
        self.allow_move_minion = self.get_tag(GameTag.ALLOW_MOVE_MINION)

        pass

    def add_hero(self, hero: HeroEntity):
        self.hero_entities[hero.entity_id] = hero
        if hero.zone == Zone.PLAY:
            if hero.own():
                self.my_hero.append(hero)
            else:
                self.enemy_hero.append(hero)
        elif hero.zone == Zone.SETASIDE:
            self.setaside_hero.append(hero)
        elif hero.zone == Zone.GRAVEYARD:
            if hero.own():
                self.dead_hero.append(hero)

        self.my_hero.sort(key=lambda x: x.zone_position)
        self.enemy_hero.sort(key=lambda x: x.zone_position)

    def get_spell_power(self, spell_school: SpellSchool):
        power = sum([h.spellpower[spell_school] for h in self.my_hero])
        # 后续操作
        return power

    def play(self, spell: SpellEntity, target: HeroEntity, own: bool):
        power = self.get_spell_power(spell.spell_school)
        pass
