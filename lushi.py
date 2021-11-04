# -*- coding: utf-8 -*-
import pyautogui
import cv2
import time
import numpy as np
import argparse
import os
import yaml
from types import SimpleNamespace
import copy

from log_util.log_util import LogUtil
from util import find_lushi_window, find_icon_location, restart_game, set_top_window, tuple_add
from battle_ai import BattleAi
from hearthstone.enums import GameTag, Zone


class Agent:
    def __init__(self, lang, basic_cfg=''):
        if lang == 'eng':
            self.cfg_file = 'config_eng.yaml'
            self.img_folder = 'imgs_eng_1024x768'
            self.title = 'hearthstone'
        elif lang == 'chs':
            self.cfg_file = 'config_chs.yaml'
            self.img_folder = "imgs_chs_1600x900"
            self.title = "炉石传说"
        else:
            raise ValueError(f"Language {lang} is not supported yet")

        self.lang = lang
        self.icons = {}
        self.treasure_blacklist = {}
        self.heros_whitelist = {}
        self.load_config(basic_cfg)
        self.log_util = LogUtil(self.basic.hs_log)
        self.game = None
        self.skill_seq_cache = {}
        self.start_seq = {}
        self.hero_info = {}
        self.side = None
        self.surprise_in_mid = False
        self.states = ['box', 'mercenaries', 'team_lock', 'travel', 'boss_list', 'team_list', 'map_not_ready',
                  'goto', 'show', 'teleport', 'start_game', 'member_not_ready', 'not_ready_dots', 'battle_ready',
                  'treasure_list', 'treasure_replace', 'destroy', 'blue_portal', 'boom', 'visitor_list',
                  'final_reward', 'final_reward2', 'final_confirm']

    def read_sub_imgs(self, sub):
        imgs = [img for img in os.listdir(os.path.join(self.img_folder, sub)) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, sub, img)), cv2.COLOR_BGR2GRAY)
            x = getattr(self, sub)
            x[k] = v

    def load_config(self, basic_cfg=''):
        with open(self.cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        if basic_cfg:
            import base64
            import json
            basic_json = json.loads(base64.b64decode(basic_cfg.encode('utf-8')).decode('utf-8'))
            self.basic = SimpleNamespace(**basic_json)
        else:
            self.basic = SimpleNamespace(**config['basic'])

        self.heros = SimpleNamespace(**config['heros'])
        self.locs = SimpleNamespace(**config['location'])
        pyautogui.PAUSE = self.basic.delay

        for sub in ['icons', 'treasure_blacklist', 'heros_whitelist']:
            self.read_sub_imgs(sub)

    def check_in_screen(self, name, prefix='icons'):
        rect, screen = find_lushi_window(self.title)
        try:
            icon = getattr(self, prefix)[name]
        except:
            return False, None, None
        success, X, Y, conf = find_icon_location(screen, icon, self.basic.confidence)
        loc = X, Y
        return success, loc, rect

    def scan_surprise_loc(self, rect):
        print('Scanning surprise')
        pyautogui.moveTo(tuple_add(rect, self.locs.scroll))
        tic = time.time()
        while True:
            success, loc, rect = self.check_in_screen('surprise')
            if success:
                print(f"Found surprise at start {loc}")
                return loc
            if self.check_in_screen('start_point')[0]:
                break
            if time.time() - tic > 10:
                return

        for _ in range(10):
            pyautogui.scroll(60)
            success, loc, rect = self.check_in_screen('surprise')
            if success:
                for _ in range(10):
                    pyautogui.scroll(-60)
                print(f"Found surprise during scrolling {loc}")
                return loc

        print("Did not found any surprise")
        return None

    def start_battle(self):
        print("Scanning battlefield")

        rect, screen = find_lushi_window(self.title)
        game = self.log_util.parse_game()

        first_x, mid_x, last_x, y = self.locs.heros
        n_my_hero = len(game.my_hero)
        is_even = n_my_hero % 2 == 0
        for i in range(n_my_hero):
            if is_even:
                x_offset = (mid_x - first_x) * (- 0.5 - n_my_hero // 2 + i + 1)
            else:
                x_offset = (mid_x - first_x) * (0 - n_my_hero // 2 + i)
            game.my_hero[i].set_pos(mid_x + x_offset + rect[0], y + rect[1])

        first_x, mid_x, last_x, y = self.locs.enemies
        n_enemy_hero = len(game.enemy_hero)
        for i in range(n_enemy_hero):
            if n_enemy_hero % 2 == 0:
                x_offset = (mid_x - first_x) * (- 0.5 - n_enemy_hero // 2 + i + 1)
            else:
                x_offset = (mid_x - first_x) * (0 - n_enemy_hero // 2 + i)
            game.enemy_hero[i].set_pos(mid_x + x_offset + rect[0], y + rect[1])

        strategy = BattleAi.battle(game.my_hero, game.enemy_hero)
        pyautogui.click(tuple_add(rect, self.locs.empty))

        if len(self.hero_info) == 0:
            for i, h in enumerate(game.hero_entities.values()):
                if i < len(self.heros.battle_seq):
                    self.skill_seq_cache[h.card_id[:-3]] = self.heros.skill_seq[i]
        else:
            for k, v in self.hero_info.items():
                self.skill_seq_cache[k] = v[-2]

        for hero_i, h in enumerate(game.my_hero):
            if h.lettuce_has_manually_selected_ability:
                continue

            pyautogui.click(h.pos)
            if h.card_id[:-3] not in self.start_seq:
                skill_loc = tuple_add(rect, (self.locs.skills[0], self.locs.skills[-1]))
            else:
                skill_loc = None
                skill_seq = self.skill_seq_cache[h.card_id[:-3]]
                for skill_id in skill_seq:
                    skill_cooldown_round = h.spell[skill_id].lettuce_current_cooldown
                    if skill_cooldown_round == 0:
                        skill_loc = tuple_add(rect, (self.locs.skills[skill_id], self.locs.skills[-1]))
                        break
            pyautogui.click(skill_loc)
            enemy_id = strategy[hero_i]
            pyautogui.click(game.enemy_hero[enemy_id].pos)
            pyautogui.click(tuple_add(rect, self.locs.empty))

    def select_members(self):
        game = self.log_util.parse_game()
        rect, screen = find_lushi_window(self.title, to_gray=False)

        if len(self.hero_info) == 0:
            for h, i in zip(game.hero_entities.values(), self.heros.battle_seq):
                self.start_seq[h.card_id[:-3]] = i
        else:
            self.heros.battle_seq = []
            hero_ids = [h.card_id[:-3] for h in game.hero_entities.values()]
            for k, v in self.hero_info.items():
                if k in hero_ids:
                    self.start_seq[k] = v[-1]
                else:
                    raise ValueError("Hero Configuration Wrong")
            for h, _ in zip(game.hero_entities.values(), self.hero_info.items()):
                self.heros.battle_seq.append(self.hero_info[h.card_id[:-3]][-1])

        hero_in_battle = [x for x in game.my_hero if x.card_id[:-3] in self.start_seq]

        if len(hero_in_battle) < 3:
            current_seq = {h.card_id[:-3]: i for i, h in enumerate(game.setaside_hero)}
            card_id_seq = [list(game.hero_entities.values())[i].card_id[:-3] for i in self.heros.battle_seq]
            card_id_seq = [x for x in card_id_seq if x in current_seq]

            for i in range(3 - len(hero_in_battle)):
                if len(card_id_seq) > 0:

                    cards_in_hand = len(card_id_seq)
                    card_id = card_id_seq.pop(0)

                    first_x, last_x, y = self.locs.members
                    mid_x = (first_x + last_x) // 2
                    current_pos = current_seq[card_id]

                    if cards_in_hand > 3:
                        dis = (last_x - first_x) // (cards_in_hand - 1)
                        loc = (first_x + dis * current_pos, y)
                    elif cards_in_hand == 3:
                        loc = (mid_x + self.locs.members_distance * (current_pos - 1), y)
                    elif cards_in_hand == 2:
                        if current_pos == 0:
                            factor = -1
                        elif current_pos == 1:
                            factor = 1
                        else:
                            raise ValueError("Not possible")

                        loc = (mid_x + self.locs.members_distance // 2 * factor, y)
                    elif cards_in_hand == 1:
                        loc = (mid_x, y)
                    else:
                        raise ValueError("Not possible")

                    pyautogui.click(tuple_add(rect, loc))
                    pyautogui.moveTo(tuple_add(rect, self.locs.dragto))
                    pyautogui.click()

                    del current_seq[card_id]
                    for k, v in current_seq.items():
                        if v > current_pos:
                            current_seq[k] = v - 1

    def state_handler(self, state, tic, text):
        success, loc, rect = self.check_in_screen(text)
        '''
        self.states = ['box', 'mercenaries', 'team_lock', 'travel', 'boss_list', 'team_list', 'map_not_ready',
                  'goto', 'show', 'teleport', 'start_game', 'member_not_ready', 'not_ready_dots', 'battle_ready',
                  'treasure_list', 'treasure_replace', 'destroy', 'blue_portal', 'boom', 'visitor_list',
                  'final_reward', 'final_reward2', 'final_confirm', 'ok', 'close']
        '''
        if success:
            if state != text:
                state = text
                tic = time.time()

            if state in ['mercenaries', 'box', 'team_lock']:
                pyautogui.click(tuple_add(rect, loc))

            if state == 'travel':
                pyautogui.click(tuple_add(rect, loc))
                pyautogui.click(tuple_add(rect, self.locs.travel))

            if state == 'boss_list':
                x_id = self.basic.boss_id % 3
                y_id = self.basic.boss_id // 3
                loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])
                pyautogui.click(tuple_add(rect, loc))
                pyautogui.click(tuple_add(rect, self.locs.start_game))

            if state == 'team_list':
                x_id = self.basic.team_id % 3
                y_id = self.basic.team_id // 3

                pyautogui.click(tuple_add(rect, (self.locs.teams[x_id], self.locs.teams[3 + y_id])))
                pyautogui.click(tuple_add(rect, self.locs.team_select))
                pyautogui.click(tuple_add(rect, self.locs.team_lock))
                surprise_loc = self.scan_surprise_loc(rect)
                if surprise_loc is not None:
                    if surprise_loc[0] < self.locs.start_point[0]:
                        self.side = 'left'
                    else:
                        self.side = 'right'
                    first_x, mid_x, last_x, y = self.locs.focus
                    if np.abs(surprise_loc[0] - mid_x) < 100:
                        self.surprise_in_mid = True
                    else:
                        self.surprise_in_mid = False
                    print(f'Surprise side {self.side}, surprise in middile {self.surprise_in_mid}')

            if state == 'map_not_ready':
                first_x, mid_x, last_x, y = self.locs.focus
                if self.side is None:
                    self.side = 'left'
                if self.side == 'left':
                    x1, x2, x3 = mid_x, (first_x + mid_x) // 2, first_x
                else:
                    x1, x2, x3 = mid_x, (last_x + mid_x) // 2, last_x
                if self.surprise_in_mid:
                    x1, x3 = x3, x1

                for x in (x1, x2, x3):
                    pyautogui.moveTo(tuple_add(rect, (x, y)))
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()

            if state in ['goto', 'show', 'teleport', 'start_game']:
                pyautogui.click(tuple_add(rect, self.locs.start_game))

            if state == 'member_not_ready':
                self.select_members()

            if state == 'not_ready_dots':
                self.start_battle()

            if state == 'battle_ready':
                pyautogui.click(tuple_add(rect, self.locs.start_battle))

            if state in ['treasure_list', 'treasure_replace']:
                while True:
                    treasure_id = np.random.randint(0, 3)
                    treasure_loc = (self.locs.treasures[treasure_id], self.locs.treasures[-1])
                    is_in_blacklilst = False
                    for key in self.treasure_blacklist.keys():
                        success, loc, rect = self.check_in_screen(key, prefix='treasure_blacklist')
                        if success:
                            x_dis = np.abs(loc[0] - treasure_loc[0])
                            if x_dis < 100:
                                is_in_blacklilst = True
                                break
                    if is_in_blacklilst:
                        continue
                    else:
                        break
                pyautogui.click(tuple_add(rect, treasure_loc))
                pyautogui.click(tuple_add(rect, self.locs.treasures_collect))

            if state in ['destroy', 'blue_portal', 'boom']:
                if self.basic.early_stop:
                    pyautogui.click(tuple_add(rect, self.locs.view_team))
                    pyautogui.click(tuple_add(rect, self.locs.give_up))
                    pyautogui.click(tuple_add(rect, self.locs.give_up_cfm))
                else:
                    pyautogui.click(tuple_add(rect, self.locs.start_game))

            if state == 'visitor_list':
                visitor_id = np.random.randint(0, 3)
                visitor_loc = (self.locs.visitors[visitor_id], self.locs.visitors[-1])
                pyautogui.click(tuple_add(rect, visitor_loc))
                pyautogui.click(tuple_add(rect, self.locs.visitors_confirm))

                for _ in range(4):
                    pyautogui.click(tuple_add(rect, self.locs.empty))

                print("Visitors Selected")
                if self.basic.early_stop:
                    print("Early stopping")
                    pyautogui.click(tuple_add(rect, self.locs.view_team))
                    pyautogui.click(tuple_add(rect, self.locs.give_up))
                    pyautogui.click(tuple_add(rect, self.locs.give_up_cfm))

            if state in ['final_reward', 'final_reward2']:
                reward_locs = eval(self.locs.rewards[self.basic.reward_count])
                for loc in reward_locs:
                    pyautogui.moveTo(tuple_add(rect, loc))
                    pyautogui.click()

                pyautogui.moveTo(tuple_add(rect, self.locs.rewards['confirm']))
                pyautogui.click()

            if state == 'final_confirm':
                pyautogui.click(tuple_add(rect, self.locs.final_confirm))

        return success, tic, state, rect

    def run(self):
        if self.basic.mode == 'pve':
            if self.basic.auto_restart:
                while True:
                    try:
                        self.run_pve()
                    except Exception as e:
                        print('错误：', e)
                        restart_game(self.lang, self.basic.bn_path)
            else:
                self.run_pve()
        elif self.basic.mode == 'pvp':
            print("PVP is no longer supported")
        else:
            raise ValueError(f"Mode {self.basic.mode} is not supported yet")

    def run_pve(self):
        time.sleep(2)
        success, loc, rect = self.check_in_screen('mercenaries')

        side = None
        surprise_in_mid = False
        tic = time.time()
        state = ""

        while True:
            pyautogui.click(tuple_add(rect, self.locs.empty))
            if time.time() - tic > self.basic.longest_waiting:
                if state == 'not_ready_dots' or state == 'member_not_ready':
                    pyautogui.click(tuple_add(rect, self.locs.options))
                    pyautogui.click(tuple_add(rect, self.locs.surrender))
                elif state == 'map_not_ready':
                    pyautogui.click(tuple_add(rect, self.locs.view_team))
                    pyautogui.click(tuple_add(rect, self.locs.give_up))
                    pyautogui.click(tuple_add(rect, self.locs.give_up_cfm))
                else:
                    restart_game(self.lang, self.basic.bn_path)
                tic = time.time()
            else:
                print(
                    f"Last state {state}, time taken: {time.time() - tic}, side: {side}, surprise_in_mid: {surprise_in_mid}")

            for state_text in self.states:
                success, tic, state, rect = self.state_handler(state, tic, state_text)
                if success:
                    pyautogui.click(tuple_add(rect, self.locs.empty))


def run_from_gui(cfg):
    if cfg['lang'].startswith('EN'):
        lang = 'eng'
    else:
        lang = 'chs'

    agent = Agent(lang=lang)
    agent.basic.boss_id = cfg['boss_id']
    agent.basic.team_id = cfg['team_id']
    agent.basic.reward_count = cfg['reward_count']
    agent.basic.bn_path = cfg['bn_path']
    agent.basic.hs_log_path = os.path.join(os.path.dirname(cfg['hs_path']), 'Logs', 'Power.log')
    agent.basic.auto_restart = cfg['auto_restart']
    agent.basic.early_stop = cfg['early_stop']
    agent.hero_info = cfg['hero']
    for k, v in agent.hero_info.items():
        agent.hero_info[k][2] = [int(x) for x in agent.hero_info[k][2].split(',')]
    agent.run()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=['eng', 'chs'], default='chs', help='Choose Your Hearthstone Language')
    parser.add_argument('--config', default='default.yaml', help='base64 basic config')
    args = parser.parse_args()

    with open(args.config, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    cfg['lang'] = args.lang
    run_from_gui(cfg)



if __name__ == '__main__':
    main()
