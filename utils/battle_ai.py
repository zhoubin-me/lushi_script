import itertools
import copy
from typing import List

from entity.hero_entity import HeroEntity
from utils.log_util import LogUtil


class BattleAi:
    def __init__(self):
        pass

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


if __name__ == '__main__':
    path = 'E:\Games\Hearthstone\Logs\Power.log'
    log = LogUtil(path)
    game = log.parse_game()
    a = BattleAi.battle(game.my_hero, game.enemy_hero)

