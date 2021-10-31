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
    def __init__(self, lang):
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
        self.is_first_battle = False
        self.icons = {}
        self.treasure_blacklist = {}
        self.heros_whitelist = {}
        self.heros_img_save = {}
        self.load_config()
        self.log_util = LogUtil(self.basic.hs_log)
        self.game = None
        self.skill_seq_cache = {}
        self.start_seq = {}

    def load_config(self):

        with open(self.cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        self.basic = SimpleNamespace(**config['basic'])
        self.heros = SimpleNamespace(**config['heros'])
        self.locs = SimpleNamespace(**config['location'])
        pyautogui.PAUSE = self.basic.delay

        imgs = [img for img in os.listdir(os.path.join(self.img_folder, 'icons')) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, 'icons', img)), cv2.COLOR_BGR2GRAY)
            self.icons[k] = v

        imgs = [img for img in os.listdir(os.path.join(self.img_folder, 'treasure_blacklist')) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, 'treasure_blacklist', img)), cv2.COLOR_BGR2GRAY)
            self.treasure_blacklist[k] = v

        imgs = [img for img in os.listdir(os.path.join(self.img_folder, 'heros_whitelist')) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, 'heros_whitelist', img)), cv2.COLOR_BGR2GRAY)
            self.heros_whitelist[k] = v

    def check_in_screen(self, name, prefix='icons'):
        icon = getattr(self, prefix)[name]
        rect, screen = find_lushi_window(self.title)
        success, X, Y, conf = find_icon_location(screen, icon, self.basic.confidence)
        loc = X, Y
        return success, loc, rect, screen

    def scan_surprise_loc(self, rect):
        print('Scanning surprise')
        pyautogui.moveTo(tuple_add(rect, self.locs.scroll))
        while True:
            result = self.check_in_screen('surprise')
            if result[0]:
                loc = result[1]
                print(f"Found surprise at start {loc}")
                return loc
            if self.check_in_screen('start_point')[0]:
                break

        for _ in range(10):
            pyautogui.scroll(60)
            result = self.check_in_screen('surprise')
            if result[0]:
                for _ in range(10):
                    pyautogui.scroll(-60)
                loc = result[1]
                print(f"Found surprise during scrolling {loc}")
                return loc

        print("Did not found any surprise")
        return None

    def start_battle(self):
        print("Scanning battlefield")

        rect, screen = find_lushi_window(self.title, to_gray=False)
        game = self.log_util.parse_game()

        first_x, mid_x, last_x, y = self.locs.heros
        n_my_hero = len(game.my_hero)
        is_even = n_my_hero % 2 == 0
        for i in range(n_my_hero):
            if is_even:
                x_offset = (mid_x - first_x) * (- 0.5 - n_my_hero // 2 + i + 1)
            else:
                x_offset = (mid_x - first_x) * (0 - n_my_hero // 2 + i)
            game.my_hero[i].set_pos(mid_x+x_offset + rect[0], y + rect[1])

        first_x, mid_x, last_x, y = self.locs.enemies
        n_enemy_hero = len(game.enemy_hero)
        is_even = n_enemy_hero % 2 == 0
        for i in range(n_enemy_hero):
            if is_even:
                x_offset = (mid_x - first_x) * (- 0.5 - n_enemy_hero // 2 + i + 1)
            else:
                x_offset = (mid_x - first_x) * (0 - n_enemy_hero // 2 + i)
            game.enemy_hero[i].set_pos(mid_x+x_offset + rect[0], y + rect[1])

        strategy = BattleAi.battle(game.my_hero, game.enemy_hero)
        pyautogui.click(tuple_add(rect, self.locs.empty))

        for i, h in enumerate(game.hero_entities.values()):
            if i < len(self.heros.battle_seq):
                self.skill_seq_cache[h.card_id] = self.heros.skill_seq[i]

        for hero_i, h in enumerate(game.my_hero):
            if h.lettuce_has_manually_selected_ability:
                continue

            pyautogui.click(h.pos)
            if h.card_id not in self.start_seq:
                skill_loc = tuple_add(rect, (self.locs.skills[0], self.locs.skills[-1]))
            else:
                skill_loc = None
                skill_seq = self.skill_seq_cache[h.card_id]
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


        for h, i in zip(game.hero_entities.values(), self.heros.battle_seq):
            self.start_seq[h.card_id] = i

        hero_in_battle = [x for x in game.my_hero if x.card_id in self.start_seq]

        if len(hero_in_battle) < 3:
            current_seq = {h.card_id: i for i, h in enumerate(game.setaside_hero)}
            card_id_seq = [list(game.hero_entities.values())[i].card_id for i in self.heros.battle_seq]
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




    def run(self):
        if self.basic.mode == 'pve':
            if self.basic.auto_restart:
                while True:
                    try:
                        self.run_pve()
                    except:
                        restart_game(self.lang, self.basic.bn_path)
            else:
                self.run_pve()
        elif self.basic.mode == 'pvp':
            print("PVP is no longer supported")
        else:
            raise ValueError(f"Mode {self.basic.mode} is not supported yet")

    def run_pve(self):
        time.sleep(2)
        result = self.check_in_screen('mercenaries')

        side = None
        surprise_in_mid = False
        tic = time.time()
        state = ""
        while True:
            pyautogui.click(tuple_add(result[2], self.locs.empty))
            if time.time() - tic > self.basic.longest_waiting:
                if state == 'not_ready_dots' or state == 'member_not_ready':
                    pyautogui.click(tuple_add(result[2], self.locs.options))
                    pyautogui.click(tuple_add(result[2], self.locs.surrender))
                elif state == 'map_not_ready':
                    pyautogui.click(tuple_add(result[2], self.locs.view_team))
                    pyautogui.click(tuple_add(result[2], self.locs.give_up))
                    pyautogui.click(tuple_add(result[2], self.locs.give_up_cfm))
                else:
                    restart_game(self.lang, self.basic.bn_path)
                tic = time.time()
            else:
                print(
                    f"Last state {state}, time taken: {time.time() - tic}, side: {side}, surprise_in_mid: {surprise_in_mid}")

            result = self.check_in_screen('mercenaries')
            if result[0]:
                pyautogui.click(tuple_add(result[1], result[2]))
                if state != "mercenaries":
                    state = "mercenaries"
                    tic = time.time()
                continue

            result = self.check_in_screen('travel')
            if result[0]:
                pyautogui.click(tuple_add(result[1], result[2]))
                pyautogui.click(tuple_add(result[2], self.locs.travel))
                if state != "travel":
                    state = "travel"
                    tic = time.time()
                continue

            result1 = self.check_in_screen('treasure_list')
            result2 = self.check_in_screen('treasure_replace')
            if result1[0] or result2[0]:
                if state != "treasure":
                    state = "treasure"
                    tic = time.time()

                while True:
                    treasure_id = np.random.randint(0, 3)
                    treasure_loc = (self.locs.treasures[treasure_id], self.locs.treasures[-1])
                    is_in_blacklilst = False
                    for key in self.treasure_blacklist.keys():
                        result3 = self.check_in_screen(key, prefix='treasure_blacklist')
                        if result3[0]:
                            x_dis = np.abs(result3[1][0] - treasure_loc[0])
                            if x_dis < 100:
                                is_in_blacklilst = True
                                break
                    if is_in_blacklilst:
                        continue
                    else:
                        break
                pyautogui.click(tuple_add(result1[2], treasure_loc))
                pyautogui.click(tuple_add(result1[2], self.locs.treasures_collect))
                continue

            result1 = self.check_in_screen('boom2')
            result2 = self.check_in_screen('ice_berg2')
            if result1[0] or result2[0]:
                if state != "boom_or_ice":
                    state = "boom_or_ice"
                    tic = time.time()

                pyautogui.click(tuple_add(result1[2], self.locs.options))

                pyautogui.click(tuple_add(result1[2], self.locs.surrender))
                continue

            result = self.check_in_screen('member_not_ready')
            if result[0]:
                if state != "member_not_ready":
                    state = "member_not_ready"
                    tic = time.time()
                self.select_members()
                continue

            result = self.check_in_screen('not_ready_dots')
            if result[0]:
                if state != "not_ready_dots":
                    state = "not_ready_dots"
                    tic = time.time()
                self.start_battle()
                self.is_first_battle = False
                continue

            result = self.check_in_screen('battle_ready')
            if result[0]:
                if state != "battle_ready":
                    state = "battle_ready"
                    tic = time.time()
                pyautogui.click(tuple_add(result[2], self.locs.start_battle))
                continue

            if self.basic.early_stop and (self.check_in_screen('destroy')[0] or
                                          self.check_in_screen('blue_portal')[0] or
                                          self.check_in_screen('boom')[0]):
                if state != "destory_blue_portal_boom":
                    state = "destory_blue_portal_boom"
                    tic = time.time()
                result = self.check_in_screen('destroy')
                pyautogui.click(tuple_add(result[2], self.locs.view_team))
                pyautogui.click(tuple_add(result[2], self.locs.give_up))
                pyautogui.click(tuple_add(result[2], self.locs.give_up_cfm))
                continue

            result = self.check_in_screen('boss_list')
            if result[0]:
                if state != "boss_list":
                    state = "boss_list"
                    tic = time.time()
                x_id = self.basic.boss_id % 3
                y_id = self.basic.boss_id // 3
                loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])
                pyautogui.click(tuple_add(result[2], loc))
                pyautogui.click(tuple_add(result[2], self.locs.start_game))
                continue

            result = self.check_in_screen('team_list')
            if result[0]:
                x_id = self.basic.team_id % 3
                y_id = self.basic.team_id // 3
                if state != "team_list":
                    state = "team_list"
                    tic = time.time()
                pyautogui.click(tuple_add(result[2], (self.locs.teams[x_id], self.locs.teams[3 + y_id])))
                pyautogui.click(tuple_add(result[2], self.locs.team_select))
                pyautogui.click(tuple_add(result[2], self.locs.team_lock))
                surprise_loc = self.scan_surprise_loc(result[2])

                if surprise_loc is not None:
                    if surprise_loc[0] < self.locs.start_point[0]:
                        side = 'left'
                    else:
                        side = 'right'
                    first_x, mid_x, last_x, y = self.locs.focus
                    if np.abs(surprise_loc[0] - mid_x) < 100:
                        surprise_in_mid = True
                    else:
                        surprise_in_mid = False
                    print(f'Surprise side {side}, surprise in middile {surprise_in_mid}')
                    continue

            result = self.check_in_screen('visitor_list')
            if result[0]:
                if state != "visitor_list":
                    state = "visitor_list"
                    tic = time.time()

                visitor_id = np.random.randint(0, 3)
                visitor_loc = (self.locs.visitors[visitor_id], self.locs.visitors[-1])
                pyautogui.click(tuple_add(result[2], visitor_loc))
                pyautogui.click(tuple_add(result[2], self.locs.visitors_confirm))

                for _ in range(5):
                    pyautogui.click(tuple_add(result[2], self.locs.empty))
                print("Visitors Selected")
                if self.basic.early_stop:
                    print("Early stopping")
                    pyautogui.click(tuple_add(result[2], self.locs.view_team))
                    pyautogui.click(tuple_add(result[2], self.locs.give_up))
                    pyautogui.click(tuple_add(result[2], self.locs.give_up_cfm))
                continue

            if self.check_in_screen('goto')[0] or \
                    self.check_in_screen('show')[0] or \
                    self.check_in_screen('collect')[0] or \
                    self.check_in_screen('teleport')[0]:
                if state != "goto_show_collect_teleport":
                    state = "goto_show_collect_teleport"
                    tic = time.time()
                result = self.check_in_screen('goto')
                pyautogui.click(tuple_add(result[2], self.locs.start_game))
                continue

            result = self.check_in_screen('start_game')
            if result[0]:
                if state != "start_game":
                    state = "start_game"
                    tic = time.time()
                pyautogui.click(tuple_add(result[2], self.locs.start_game))
                self.is_first_battle = True
                continue

            result1 = self.check_in_screen('final_reward')
            result2 = self.check_in_screen('final_reward2')
            if result1[0] or result2[0]:
                if state != "final_reward":
                    state = "final_reward"
                    tic = time.time()
                reward_locs = eval(self.locs.rewards[self.basic.reward_count])
                for loc in reward_locs:
                    pyautogui.moveTo(tuple_add(result1[2], loc))
                    pyautogui.click()

                pyautogui.moveTo(tuple_add(result1[2], self.locs.rewards['confirm']))
                pyautogui.click()
                continue

            result = self.check_in_screen('final_confirm')
            if result[0]:
                if state != "final_confirm":
                    state = "final_confirm"
                    tic = time.time()
                pyautogui.click(tuple_add(result[2], self.locs.final_confirm))
                continue

            result = self.check_in_screen('map_not_ready')
            if result[0]:
                if state != "map_not_ready":
                    state = "map_not_ready"
                    tic = time.time()
                first_x, mid_x, last_x, y = self.locs.focus
                if side is None:
                    side = 'left'
                if side == 'left':
                    x1, x2, x3 = mid_x, (first_x + mid_x) // 2, first_x
                else:
                    x1, x2, x3 = mid_x, (last_x + mid_x) // 2, last_x

                if surprise_in_mid:
                    x1, x3 = x3, x1

                for x in (x1, x2, x3):
                    pyautogui.moveTo(tuple_add(result[2], (x, y)))
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                continue

            pyautogui.click(tuple_add(result[2], self.locs.empty))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=['eng', 'chs'], default='chs', help='Choose Your Hearthstone Language')
    args = parser.parse_args()

    agent = Agent(lang=args.lang)
    agent.run()


if __name__ == '__main__':
    main()
