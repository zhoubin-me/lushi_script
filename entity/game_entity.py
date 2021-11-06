from typing import Dict, List

from hearthstone.entities import Entity
from hearthstone.enums import GameTag, Zone, SpellSchool

from .action import Action
from .base_entity import BaseEntity
from .hero_entity import HeroEntity
from .spell_entity import SpellEntity


class GameEntity(BaseEntity):

    def __init__(self, entity: Entity):
        super().__init__(entity)
        # 0 我方场上信息 1敌方场上信息
        self.players = self.entity.players
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
        # 当前回合的敌方action列表
        self.enemy_action_list = []
        # 当前回合的我方action列表
        self.my_action_list = []
        # 当前回合的action列表
        self.all_action_list = []
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

    def get_spell_power(self, spell_school: SpellSchool, own=True):
        player = self.players[0] if own else self.players[1]
        pd = {
            SpellSchool.NONE: GameTag.CURRENT_SPELLPOWER,
            SpellSchool.ARCANE: GameTag.CURRENT_SPELLPOWER_ARCANE,
            SpellSchool.FIRE: GameTag.CURRENT_SPELLPOWER_FIRE,
            SpellSchool.FROST: GameTag.CURRENT_SPELLPOWER_FROST,
            SpellSchool.NATURE: GameTag.CURRENT_SPELLPOWER_NATURE,
            SpellSchool.HOLY: GameTag.CURRENT_SPELLPOWER_HOLY,
            SpellSchool.SHADOW: GameTag.CURRENT_SPELLPOWER_SHADOW,
            SpellSchool.FEL: GameTag.CURRENT_SPELLPOWER_FEL,
            SpellSchool.PHYSICAL_COMBAT: GameTag.CURRENT_SPELLPOWER_PHYSICAL
        }
        power = player.tags.get(pd.get(spell_school)) or 0
        # 后续操作
        return power

    def get_player_tag(self, player, tag_name):
        return player.tags.get(tag_name) or 0

    def get_action_list(self, own=True):
        return self.my_action_list if own else self.enemy_action_list

    def get_hero_list(self, own=True):
        return self.my_hero if own else self.enemy_hero

    def can_combo(self, spell: SpellEntity, spell_school=None, own=True):
        action_list = self.get_action_list(own)
        if len(action_list) <= 0:
            return False
        if spell_school is None:
            return action_list[0].entity_id != spell.entity_id
        else:
            for action in action_list:
                if action.spell.entity_id == spell.entity_id:
                    return False
                if action.spell.spell_school == spell_school:
                    return True

    def get_enemy_action(self):
        if len(self.enemy_action_list):
            return self.enemy_action_list
        action = []
        for h in self.enemy_hero:
            spell = h.get_enemy_action()
            action.append(Action(hero=h, spell=spell, target=self.find_min_health()))
            self.action_list = action
        return action

    def find_min_health(self, own=True):
        """
        查找敌我场上生命值最低的佣兵, 默认我方
        Args:
            own: 是否是我方场上
        """
        hero_list = self.my_hero if own else self.enemy_hero
        if len(hero_list) <= 0:
            return None
        return min(hero_list, key=lambda x: x.get_health())

    def play(self, hero: HeroEntity, spell: SpellEntity, target: HeroEntity):
        power = self.get_spell_power(spell.spell_school)
        spell.play(hero, target)
        pass

    def do_action(self, action):
        # 回合开始
        # 技能施放
        # 受伤扳机
        # 检测死亡
        # 亡语扳机
        # 回合结束
        pass
