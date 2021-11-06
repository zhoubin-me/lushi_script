import itertools
import copy
from typing import List

from entity.action import Action
from entity.game_entity import GameEntity
from entity.hero_entity import HeroEntity
from entity.spell_entity import SpellEntity
from utils.log_util import LogUtil


class BattleAi:
    def __init__(self):
        self.game: GameEntity = None
        self.score = -10000
        self.action = []
        pass

    @classmethod
    def from_game(cls, game):
        ba = BattleAi()
        ba.game = game
        return ba

    @staticmethod
    def analyze_score(my_list, enemy_list):
        """
        我方尽量不死，且血量最多，敌方尽量死且剩余血量最少
        我方数量 * (我方血量最低值 + 我方血量总值)   -  (敌方血量最高值 + 敌方血量总值) * 敌方数量
        """
        my_health = [x.get_health() for x in my_list if x.get_health() > 0]
        enemy_health = [x.get_health() for x in enemy_list if x.get_health() > 0]
        my_cnt = len(my_health)
        my_min_health = min(my_health) if len(my_health) > 0 else 0
        my_sum_health = sum(my_health) if len(my_health) > 0 else 0
        enemy_cnt = len(enemy_health)
        enemy_max_health = max(enemy_health) if len(enemy_health) > 0 else 0
        enemy_health = sum(enemy_health) if len(enemy_health) > 0 else 0
        score = my_cnt * (my_min_health + my_sum_health) - (enemy_max_health + enemy_health) * enemy_cnt
        return score

    @staticmethod
    def battle(my_hero: List[HeroEntity], enemy_hero: List[HeroEntity]):

        optimal_strategy = ((-1 << 25), [1, 1, 1])
        for idx in list(itertools.product(range(len(enemy_hero)), repeat=len(my_hero))):
            my = copy.deepcopy(my_hero)
            enemy = copy.deepcopy(enemy_hero)
            for i, target in enumerate(idx):
                my[i].basic_attack(enemy[target], my[i].atk)
            for i, e in enumerate(enemy):
                if e.get_health() > 0:
                    my_min_health_hero = BattleAi.find_min_health(my)
                    e.basic_attack(my_min_health_hero, e.atk)

            score = BattleAi.analyze_score(my, enemy)
            if score > optimal_strategy[0]:
                optimal_strategy = (score, idx)

        return {k: v for k, v in enumerate(optimal_strategy[1])}

    @staticmethod
    def find_min_health(heros):
        return min(heros, key=lambda x: x.get_health())

    def reset(self):
        self.score = -1 << 25
        self.action.clear()

    def battle2(self):
        self.reset()
        self.dfs(0, [])
        # print(self.score)
        # for x in self.action:
        #     print(x.hero, x.target, x.spell, end='\n\n\n')
        return self.action

    def simulate_battle(self, action_list):
        _game = copy.deepcopy(game)
        all_action_list = copy.deepcopy(action_list)
        _game.my_action_list = copy.deepcopy(action_list)
        all_action_list.extend(_game.get_enemy_action())
        all_action_list.sort()
        _game.all_action_list = all_action_list
        for x in all_action_list:
            if not x.hero.is_alive():
                continue
            # print(x['hero'], x['target'], x['spell'], end='\n\n\n')
            hero = _game.get_hero_by_eid(x.hero.entity_id)
            target = None
            spell = hero.get_spell_by_eid(x.spell.entity_id)
            if x.target is not None:
                target = _game.get_hero_by_eid(x.target.entity_id)
            _game.play(_game, hero, spell, target)
        score = self.analyze_score(_game.my_hero, _game.enemy_hero)
        # print(score)
        if self.score < score:

            self.score = score
            self.action = copy.deepcopy(action_list)
            self.action.sort()
        pass

    def dfs(self, hero_id, result: List):
        # 枚举英雄
        if hero_id >= len(self.game.my_hero):
            self.simulate_battle(copy.deepcopy(result))
            return
        hero = self.game.my_hero[hero_id]
        # 枚举技能
        spell_list = hero.get_available_spell_list()
        for spell in spell_list:
            # 枚举目标
            if spell.damage >= 0:
                if spell.range == 1:
                    for enemy in self.game.enemy_hero:
                        # 对哪个目标使用哪个技能
                        result.append(Action(hero=hero, spell=spell, target=enemy))
                        self.dfs(hero_id + 1, result)
                        result.pop()
                else:
                    result.append(Action(hero=hero, spell=spell, target=None))
                    self.dfs(hero_id + 1, result)
                    result.pop()
            else:
                for my in game.my_hero:
                    pass
        pass


if __name__ == '__main__':
    path = 'D:\\Hearthstone\\Logs\\Power.log'
    log = LogUtil(path)
    game = log.parse_game()
    # a = BattleAi.battle(game.my_hero, game.enemy_hero)
    # print(a)
    ai = BattleAi.from_game(game)
    ai.battle2()
