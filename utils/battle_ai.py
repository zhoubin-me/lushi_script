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
    def analyze_score(my_list, enemy_list, skip_our_health = False):
        """
        我方尽量不死，且血量最多，敌方尽量死且剩余血量最少
        score = 我方数量 * (我方血量最低值 + 我方血量总值)   -  (敌方血量最高值 + 敌方血量总值) * 敌方数量

        skip_our_health: 自己扛的住，不考虑生存，伤害最大策略。 
        score = -  (敌方血量最高值 + 敌方血量总值) * 敌方数量
        """
        my_health = [x.get_health() for x in my_list if x.get_health() > 0]
        enemy_health = [x.get_health() for x in enemy_list if x.get_health() > 0]
        my_cnt = len(my_health)
        my_min_health = min(my_health) if len(my_health) > 0 else 0
        my_sum_health = sum(my_health) if len(my_health) > 0 else 0
        enemy_cnt = len(enemy_health)
        enemy_max_health = max(enemy_health) if len(enemy_health) > 0 else 0
        enemy_health = sum(enemy_health) if len(enemy_health) > 0 else 0
        if skip_our_health == True :
            score = - (enemy_max_health + enemy_health) * len(enemy_list) # 这里不考虑干死
            return score
        else :
            score =  my_cnt * (my_min_health + my_sum_health) - (enemy_max_health + enemy_health) * enemy_cnt
            return score

    @staticmethod
    def analyze_max_dmg(my_list, enemy_list):
        """
        打出暴击，尽量打同一个。集火速度慢的，慢速基本是大招。
        同色队列，先打优先级队列里的。最后打低优先级的。
        """
        last_enemy_list = [
            "LETLT_108_01" # 冰血要塞
            ]
        first_enemy_list = [
            "LETLT_117_01"  # 冰冻猛犸象
            "LETLT_100_01"  # 双倍攻击剑圣
        ]
        attatch_sequnce = []
        lettuce_enemy_map = {3: [], 1: [], 2: [], 4: [], 0: [], "all": []}

        i = -1
        for v in enemy_list:
            i += 1
            if v.card_id in first_enemy_list :
                lettuce_enemy_map[v.lettuce_role].insert(0, i)
                lettuce_enemy_map["all"].insert(0, i)
                continue
            elif v.card_id in last_enemy_list :
                continue
            
            lettuce_enemy_map[v.lettuce_role].append(i)
            lettuce_enemy_map["all"].append(i)
        
        # 最后的加进来
        i = 0
        for v in enemy_list:
            if v.card_id in last_enemy_list :
                lettuce_enemy_map[v.lettuce_role].append(i)
                lettuce_enemy_map["all"].append(i)
            
            i += 1
        # 去重复
        lettuce_enemy_map["all"] = list(dict.fromkeys(lettuce_enemy_map["all"]))

        for v in my_list:
            if 1 == v.lettuce_role:
                if 0 < len(lettuce_enemy_map[3]):
                    attatch_sequnce.append(lettuce_enemy_map[3][0])
                else :
                    attatch_sequnce.append(lettuce_enemy_map["all"][0])
            elif 2 == v.lettuce_role:
                if  0 < len(lettuce_enemy_map[1]):
                    attatch_sequnce.append(lettuce_enemy_map[1][0])
                else:
                    attatch_sequnce.append(lettuce_enemy_map["all"][0])
            elif 3 == v.lettuce_role:
                if 0 < len(lettuce_enemy_map[2]):
                    attatch_sequnce.append(lettuce_enemy_map[2][0])
                else:
                    attatch_sequnce.append(lettuce_enemy_map["all"][0])
            else:
                attatch_sequnce.append(lettuce_enemy_map["all"][0])

        return attatch_sequnce

    @staticmethod
    def battle(my_hero: List[HeroEntity], enemy_hero: List[HeroEntity], stratege_intervene = "normal"):
        if "kill_big" == stratege_intervene : # 先干最大的
            boss_id = -1
            max_health = 0
            i = 0
            for e_hero in enemy_hero:
                if e_hero.get_max_health() > max_health:
                    boss_id  = i
                    max_health = e_hero.get_max_health()
                i += 1
            return [boss_id, boss_id, boss_id, boss_id, boss_id, boss_id]
        elif "kill_min" == stratege_intervene : # 先干最小的
            suite_id = -1
            min_health = 10000
            i = 0
            for e_hero in enemy_hero:
                if e_hero.get_max_health() < min_health:
                    suite_id  = i
                    min_health = e_hero.get_max_health()
                i += 1
            return [suite_id, suite_id, suite_id, suite_id, suite_id, suite_id]
        elif "max_dmg" == stratege_intervene:
            re = BattleAi.analyze_max_dmg(my_hero, enemy_hero)
            print(f"battle strateg max_dmg: {re}")
            return re
        else : # normal, max_dmg
            optimal_strategy = ((-1 << 25), [1, 1, 1])
            for idx in list(itertools.product(range(len(enemy_hero)), repeat=len(my_hero))):
                my = copy.deepcopy(my_hero)
                enemy = copy.deepcopy(enemy_hero)
                for i, target in enumerate(idx):
                    my[i].basic_attack(enemy[target], my[i].atk)
                for i, e in enumerate(enemy):
                    if e.get_health() > 0:
                        my_min_health_hero = BattleAi.find_min_health(my)
                        if my_min_health_hero is None:
                            continue
                        e.basic_attack(my_min_health_hero, e.atk)
                score = -999999
                if "max_dmg" == stratege_intervene:
                    score = BattleAi.analyze_score(my, enemy, True)
                else :
                    score = BattleAi.analyze_score(my, enemy)
                if score > optimal_strategy[0]:
                    optimal_strategy = (score, idx)

            return {k: v for k, v in enumerate(optimal_strategy[1])}

    @staticmethod
    def battle_boss(my_hero: List[HeroEntity], enemy_hero: List[HeroEntity]):
        boss_id = -1
        max_health = 0
        i = 0
        for e_hero in enemy_hero:
            if e_hero.get_max_health() > max_health:
                boss_id  = i
            i += 1
        
        return [boss_id, boss_id, boss_id]

    @staticmethod
    def find_min_health(heros):
        if len(heros) <= 0:
            return None
        return min(heros, key=lambda x: x.get_health())

    def reset(self):
        self.score = -1 << 25
        self.action.clear()

    def battle2(self):
        self.reset()
        self.dfs(0, [])
        print(self.score)
        for x in self.action:
            print(x.hero, x.target, x.spell, end='\n\n\n')
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
            # if score == 942:
            #     for h in _game.enemy_hero:
            #         print(h.get_health())
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
    path = 'C:\\var\\Hearthstone\\Logs\\Power.log'
    log = LogUtil(path)
    game = log.parse_game()
    # a = BattleAi.battle(game.my_hero, game.enemy_hero)
    # print(a)
    ai = BattleAi.from_game(game)
    ai.battle2()
