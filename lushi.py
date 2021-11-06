# -*- coding: utf-8 -*-
import pyautogui
import cv2
import time
import numpy as np
import argparse
import os
import yaml
from types import SimpleNamespace

from utils.log_util import LogUtil
from utils.util import find_lushi_window, find_icon_location, restart_game, tuple_add, find_relative_loc
from utils.battle_ai import BattleAi


class Agent:
    def __init__(self, cfg):
        if cfg['lang'].startswith('EN'):
            self.lang = 'eng'
            self.loc_file = 'config/locs_eng.yaml'
            self.img_folder = 'resource/imgs_eng_1024x768'
            self.title = 'hearthstone'
        elif cfg['lang'].startswith('ZH'):
            self.lang = 'chs'
            self.loc_file = 'config/locs_chs.yaml'
            self.img_folder = "resource/imgs_chs_1600x900"
            self.title = "炉石传说"
        else:
            raise ValueError(f"Language {cfg['lang']} is not supported yet")



        self.icons = {}
        self.treasure_blacklist = {}
        self.heros_whitelist = {}
        self.game = None
        self.skill_seq_cache = {}
        self.start_seq = {}
        self.side = None
        self.surprise_in_mid = False
        self.states = ['box', 'mercenaries', 'team_lock', 'travel', 'boss_list', 'team_list', 'map_not_ready',
                       'goto', 'show', 'teleport', 'start_game', 'member_not_ready', 'not_ready_dots', 'battle_ready',
                       'treasure_list', 'treasure_replace', 'destroy', 'blue_portal', 'boom', 'visitor_list',
                       'final_reward', 'final_reward2', 'final_confirm']

        self.load_config(cfg)
        self.log_util = LogUtil(self.basic.hs_log)

    def read_sub_imgs(self, sub):
        imgs = [img for img in os.listdir(os.path.join(self.img_folder, sub)) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, sub, img)), cv2.COLOR_BGR2GRAY)
            x = getattr(self, sub)
            x[k] = v

    def load_config(self, cfg):
        with open(self.loc_file, 'r', encoding='utf-8') as f:
            loc_cfg = yaml.safe_load(f)

        self.locs = SimpleNamespace(**loc_cfg['location'])
        for sub in ['icons', 'treasure_blacklist', 'heros_whitelist']:
            self.read_sub_imgs(sub)

        hero_info = cfg['hero']
        self.heros = {}
        for k, v in hero_info.items():
            spell_order = [int(x)-1 for x in v[2].split(',')]
            self.heros[k] = [v[0],  v[1], spell_order, v[3]]
            self.skill_seq_cache[k] = v[-2]
        del cfg['hero']
        cfg['hs_log'] = os.path.join(os.path.dirname(cfg['hs_path']), 'Logs', 'Power.log')
        self.basic = SimpleNamespace(**cfg)
        pyautogui.PAUSE = self.basic.delay

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

        for hero_i, h in enumerate(game.my_hero):
            if h.lettuce_has_manually_selected_ability:
                continue

            pyautogui.click(h.pos)
            card_id = h.card_id[:-3]
            if card_id not in self.heros:
                skill_loc = tuple_add(rect, (self.locs.skills[0], self.locs.skills[-1]))
            else:
                skill_loc = None
                skill_seq = self.heros[card_id][-2]
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

        hero_in_battle = [h for h in game.my_hero if h.card_id[:-3] in self.heros]
        if len(hero_in_battle) < 3:
            current_seq = {h.card_id[:-3]: i for i, h in enumerate(game.setaside_hero)}
            heros_sorted = {k: v[-1] for k, v in sorted(
                self.heros.items(), key=lambda item: item[1][-1])}
            card_id_seq = list(heros_sorted.keys())
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
        if self.basic.auto_restart:
            while True:
                try:
                    self.run_pve()
                except Exception as e:
                    print('错误：', e)
                    restart_game(self.lang, self.basic.bn_path)
        else:
            self.run_pve()

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
    print(cfg)
    if cfg['lang'].startswith('EN'):
        lang = 'eng'
    elif cfg['lang'].startswith('ZH'):
        lang = 'chs'
    else:
        lang = None
    restart_game(lang, cfg['bn_path'], kill_existing=False)
    agent = Agent(cfg=cfg)
    agent.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=['chs', 'eng'], default='chs', help='Choose Your Hearthstone Language')
    parser.add_argument('--config', default='config/default.yaml', help='launch config filename')
    parser.add_argument('--func', choices=['run', 'coor'], help='Run main function or find coordinates')
    args = parser.parse_args()

    if args.func == 'run':
        with open(args.config, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)

        if args.lang == 'chs':
            cfg['lang'] = 'ZH-1600x900'
        else:
            cfg['lang'] = 'EN-1024x768'

        run_from_gui(cfg)
    elif args.func == 'coor':
        if args.lang == 'chs':
            title = '炉石传说'
        elif args.lang == 'eng':
            title = 'Hearthstone'
        else:
            title = None
        while True:
            find_relative_loc(title)
            time.sleep(1)

if __name__ == '__main__':
    main()
