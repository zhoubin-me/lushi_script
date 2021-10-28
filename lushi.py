# -*- coding: utf-8 -*-
import pyautogui
import cv2
import time
import numpy as np
import argparse
import os
import yaml
from types import SimpleNamespace
from PIL import ImageGrab

from util import find_lushi_window, find_icon_location, restart_game, set_top_window, tuple_add
from img_proc import analyse_battle_field

class Agent:
    def __init__(self, lang):
        self.lang = lang
        self.icons = {}
        self.treasure_blacklist = {}
        self.heros_whitelist = {}
        self.load_config()

    def load_config(self):
        if self.lang == 'eng':
            cfg_file = 'config_eng.yaml'
            img_folder = 'imgs_eng_1024x768'
            self.title = 'hearthstone'
        elif self.lang == 'chs':
            cfg_file = 'config_chs.yaml'
            img_folder = "imgs_chs_1600x900"
            self.title = "炉石传说"
        else:
            raise ValueError(f"Language {self.lang} is not supported yet")

        with open(cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        self.basic = SimpleNamespace(**config['basic'])
        self.heros = SimpleNamespace(**config['heros'])
        self.locs = SimpleNamespace(**config['location'])
        self.retry = SimpleNamespace(**config['retry'])
        pyautogui.PAUSE = self.basic.delay

        imgs = [img for img in os.listdir(os.path.join(img_folder, 'icons')) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(img_folder, 'icons', img)), cv2.COLOR_BGR2GRAY)
            self.icons[k] = v

        imgs = [img for img in os.listdir(os.path.join(img_folder, 'treasure_blacklist')) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(img_folder, 'treasure_blacklist', img)), cv2.COLOR_BGR2GRAY)
            self.treasure_blacklist[k] = v

        imgs = [img for img in os.listdir(os.path.join(img_folder, 'heros_whitelist')) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(img_folder, 'heros_whitelist', img)), cv2.COLOR_BGR2GRAY)
            self.heros_whitelist[k] = v
        set_top_window(self.title)

    def check_in_screen(self, icon_name):
        icon = self.icons[icon_name]
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

    def start_battle(self, rect):
        time.sleep(5)
        pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
        rect, screen = find_lushi_window(self.title, to_gray=False)
        hero_info = analyse_battle_field(self.locs.hero_region, screen)
        enemy_info = analyse_battle_field(self.locs.enemy_region, screen)
        enemy_info.sort(key=lambda x: x[4])
        hero_info.sort(key=lambda x: x[4])

        width, height = self.locs.skill_waiting

        for hero_i, hero_x, hero_y, damage, health, color in hero_info:
            pyautogui.moveTo(tuple_add((hero_x, hero_y), rect))
            pyautogui.click()

            skill_idx = 0
            for skill_id in self.heros.skill_priority[hero_i]:
                skill_loc = tuple_add(rect, (self.locs.skills[skill_id], self.locs.skills[-1]))

                region = tuple_add(skill_loc, (-width//2, -height)) + tuple_add(skill_loc, (width//2, 0))
                skill_img = cv2.cvtColor(np.array(ImageGrab.grab(region)), cv2.COLOR_RGB2GRAY)
                found, _, _, _  = find_icon_location(skill_img, self.icons['skill_waiting'], self.basic.confidence)
                if not found:
                    pyautogui.click(skill_loc)
                    skill_idx = skill_id
                    break

            if self.heros.skill_basic_damage[hero_i][skill_idx] > 0:
                target_i = 0
                for enemy_i, (_, enemy_x, enemy_y, damage_e, health_e, color_e) in enumerate(enemy_info):
                    if color == 'r' and color_e == 'g' or color == 'b' and color_e == 'r' or color == 'g' and color_e == 'b':
                        target_i = enemy_i
                        break
                target_loc = tuple_add(rect, enemy_info[target_i][1:3])
            else:
                target_loc = tuple_add(rect, hero_info[0][1:3])
            pyautogui.click(target_loc)


    def run_pvp(self):
        self.basic.reward_count = 5
        state = ""
        tic = time.time()
        rect, screen = find_lushi_window(self.title)
        while True:
            pyautogui.click(tuple_add(rect, self.locs.empty))
            time.sleep(self.basic.delay + np.random.rand())

            if time.time() - tic > self.basic.longest_waiting:
                restart_game(self.lang, self.basic.battle_net_path)
                tic = time.time()
<<<<<<< Updated upstream

=======
            
>>>>>>> Stashed changes
            result = self.check_in_screen('mercenaries')
            if result[0]:
                pyautogui.click(result[1])
                if state != "mercenaries":
                    state = "mercenaries"
                    tic = time.time()
                continue

            result = self.check_in_screen('pvp')
            if result[0]:
                pyautogui.click(result[1])
                if state != "pvp":
                    state = "pvp"
                    tic = time.time()
                continue

            result = self.check_in_screen('pvp_team')
            if result[0]:
                pyautogui.click(tuple_add(result[2], self.locs.team_select))
                if state != "pvp_team":
                    state = "pvp_team"
                    tic = time.time()
                continue
<<<<<<< Updated upstream

=======
            
>>>>>>> Stashed changes
            result1 = self.check_in_screen('pvp_ready')
            result2 = self.check_in_screen('member_not_ready')
            if result1[0] or result2[0]:
                print("Surrendering")
                pyautogui.click(tuple_add(result1[2], self.locs.options))
                time.sleep(self.basic.pvp_delay)
                if self.basic.fast_surrender:
                    pyautogui.click(tuple_add(result1[2], self.locs.surrender))
                else:
                    result = self.check_in_screen('surrender')

                    if result[0]:
                        pyautogui.click(result[1])

                for _ in range(5):
                    pyautogui.click(tuple_add(result1[0] + self.locs.empty))

                if state != "pvp_ready":
                    state = "pvp_ready"
                    tic = time.time()
                continue

            result1 = self.check_in_screen('final_reward')
            result2 = self.check_in_screen('final_reward2')
            if result1[0] or result2[0]:
                reward_locs = eval(self.locs.rewards[self.basic.reward_count])
                for loc in reward_locs:
                    pyautogui.moveTo(tuple_add(result1[1] + loc))
                    pyautogui.click()

                pyautogui.moveTo(tuple_add(result1[1] + self.locs.rewards['final_confirm']))
                pyautogui.click()

                for _ in range(5):
                    pyautogui.click(tuple_add(result1[1] + self.locs.empty))
                if state != "final_reward":
                    state = "final_reward"
                    tic = time.time()
                continue

            if state != "":
                state = ""
                tic = time.time()


    def run_pve(self):
        side = None
        surprise_in_mid = False
        rect, screen = find_lushi_window(self.title)
        while True:
            pyautogui.click(tuple_add(rect, self.locs.empty))
            time.sleep(np.random.rand() + self.basic.delay)

            result = self.check_in_screen('mercenaries')
            if result[0]:
                pyautogui.click(result[1])
                if state != "mercenaries":
                    state = "mercenaries"
                    tic = time.time()
                continue

            if 'travel' in states:
                pyautogui.click(states['travel'][0])
                pyautogui.click(rect[0] + self.locs.travel[0], rect[1] + self.locs.travel[1])
                continue

            if 'treasure_list' in states or 'treasure_replace' in states:
                while True:
                    treasure_id = np.random.randint(0, 3)
                    treasure_loc = (self.locs.treasures[treasure_id], self.locs.treasures[-1])

                    is_in_blacklilst = False
                    for key in self.treasure_blacklist.keys():
                        if key in states:
                            x_dis = np.abs(treasure_loc[0] + rect[0] - states[key][0][0])
                            if x_dis < 100:
                                is_in_blacklilst = True
                                break

                    if is_in_blacklilst:
                        continue
                    else:
                        break

                pyautogui.click(rect[0] + treasure_loc[0], rect[1] + treasure_loc[1])
                pyautogui.click(rect[0] + self.locs.treasures_collect[0], rect[1] + self.locs.treasures_collect[1])

            if 'boom2' in states or 'ice_berg2' in states:
                print("Surrendering", states)
                pyautogui.click(rect[0] + self.locs.options[0], rect[1] + self.locs.options[1])
                pyautogui.click(rect[0] + self.locs.surrender[0], rect[1] + self.locs.surrender[1])
                continue

            if 'member_not_ready' in states:
                first_x, last_x, y = self.locs.members
                mid_x = (first_x + last_x) // 2
                for i, idx in enumerate(self.heros.start_priority):
                    current_heros_left = self.basic.hero_count - i
                    if current_heros_left > 3:
                        dis = (last_x - first_x) // (self.basic.hero_count - i - 1)
                        loc = (first_x + dis * (idx - i), y)
                    elif current_heros_left == 3:
                        loc = (mid_x + self.locs.members_distance * (idx - i - 1), y)
                    elif current_heros_left == 2:
                        if idx - i - 1 == 0:
                            factor = 1
                        else:
                            factor = -1
                        loc = (mid_x + self.locs.members_distance // 2 * factor, y)
                    elif current_heros_left == 1:
                        loc = (mid_x, y)
                    pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                    pyautogui.moveTo(rect[0] + self.locs.dragto[0], rect[1] + self.locs.dragto[1])
                    pyautogui.click()
                continue

            if 'not_ready_dots' in states:
                self.start_battle(rect)
                continue

            if 'battle_ready' in states:
                pyautogui.click(states['battle_ready'][0])
                continue

            if ('destroy' in states or 'blue_portal' in states or 'boom' in states) and self.basic.early_stop:
                pyautogui.click(self.locs.view_team[0] + rect[0], self.locs.view_team[1] + rect[1])
                pyautogui.click(self.locs.give_up[0] + rect[0], self.locs.give_up[1] + rect[1])
                pyautogui.click(self.locs.give_up_cfm[0] + rect[0], self.locs.give_up_cfm[1] + rect[1])
                continue

            if 'boss_list' in states:
                x_id = self.basic.boss_id % 3
                y_id = self.basic.boss_id // 3
                loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])
                pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                pyautogui.click(rect[0] + self.locs.start_game[0], rect[1] + self.locs.start_game[1])
                continue

            if 'team_list' in states:
                x_id = self.basic.team_id % 3
                y_id = self.basic.team_id // 3
                pyautogui.click(rect[0] + self.locs.teams[x_id], rect[1] + self.locs.teams[3 + y_id])
                pyautogui.click(rect[0] + self.locs.team_select[0], rect[1] + self.locs.team_select[1])
                pyautogui.click(rect[0] + self.locs.team_lock[0], rect[1] + self.locs.team_lock[1])
                surprise_loc = self.scan_surprise_loc(rect)

                if surprise_loc is not None:
                    if surprise_loc[0] < self.locs.start_point[0] + rect[0]:
                        side = 'left'
                    else:
                        side = 'right'
                    first_x, mid_x, last_x, y = self.locs.focus
                    if np.abs(surprise_loc[0] - rect[0] - mid_x) < 90:
                        surprise_in_mid = True
                    else:
                        surprise_in_mid = False
                    continue

            if 'visitor_list' in states:
                for key in self.heros_whitelist.keys():
                    if key in states:
                        pyautogui.click(states[key][0])
                        pyautogui.click(rect[0] + self.locs.visitors_confirm[0],
                                        rect[1] + self.locs.visitors_confirm[1])
                        break
                else:
                    visitor_id = np.random.randint(0, 3)
                    visitor_loc = (self.locs.visitors[visitor_id], self.locs.visitors[-1])
                    pyautogui.click(rect[0] + visitor_loc[0], rect[1] + visitor_loc[1])
                    pyautogui.click(rect[0] + self.locs.visitors_confirm[0], rect[1] + self.locs.visitors_confirm[1])

                for _ in range(5):
                    pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
                print("Visitors Selected")
                if self.basic.early_stop:
                    print("Early stopping")
                    pyautogui.click(self.locs.view_team[0] + rect[0], self.locs.view_team[1] + rect[1])
                    pyautogui.click(self.locs.give_up[0] + rect[0], self.locs.give_up[1] + rect[1])
                    pyautogui.click(self.locs.give_up_cfm[0] + rect[0], self.locs.give_up_cfm[1] + rect[1])
                continue

            if 'goto' in states or 'show' in states or 'collect' in states or 'teleport' in states:
                pyautogui.click(rect[0] + self.locs.start_game[0], rect[1] + self.locs.start_game[1])
                continue

            if 'start_game' in states:
                pyautogui.click(rect[0] + self.locs.start_game[0], rect[1] + self.locs.start_game[1])
                battle_round_count = 0
                skill_selection_retry = 0
                heroes_selection_retry = 0
                find_map_entry_retry = 0
                continue

            if 'final_reward' in states or 'final_reward2' in states:
                reward_locs = eval(self.locs.rewards[self.basic.reward_count])
                for loc in reward_locs:
                    pyautogui.moveTo(rect[0] + loc[0], rect[1] + loc[1])
                    pyautogui.click()
                pyautogui.moveTo(rect[0] + self.locs.rewards['confirm'][0], rect[1] + self.locs.rewards['confirm'][1])
                pyautogui.click()
                continue

            if 'final_confirm' in states:
                pyautogui.click(rect[0] + self.locs.final_confirm[0], rect[1] + self.locs.final_confirm[1])
                continue

            if 'map_not_ready' in states and 'final_boss' in states:
                pyautogui.moveTo(rect[0] + self.locs.final_boss[0], rect[1] + self.locs.final_boss[1])
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                time.sleep(self.basic.delay)
                states, rect, screen = self.check_state()
                if 'start_game' in states:
                    pyautogui.click(rect[0] + self.locs.start_game[0], rect[1] + self.locs.start_game[1])
                    continue

            if 'map_not_ready' in states:
                if find_map_entry_retry > self.retry.map_ready:
                    # early stop
                    pyautogui.click(self.locs.view_team[0] + rect[0], self.locs.view_team[1] + rect[1])
                    pyautogui.click(self.locs.give_up[0] + rect[0], self.locs.give_up[1] + rect[1])
                    pyautogui.click(self.locs.give_up_cfm[0] + rect[0], self.locs.give_up_cfm[1] + rect[1])
                    find_map_entry_retry = 0
                    continue
                print('Looking for next fight, attempt', find_map_entry_retry)
                find_map_entry_retry += 1
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
                    pyautogui.moveTo(x + rect[0], y + rect[1])
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=['eng', 'chs'], default='chs', help='Choose Your Hearthstone Language')
    args = parser.parse_args()

    agent = Agent(lang=args.lang)
    if agent.basic.mode == 'pve':
        agent.run_pve()
    elif agent.basic.mode == 'pvp':
        agent.run_pvp()
    else:
        raise ValueError(f"Mode {agent.basic.mode} is not supported yet")


if __name__ == '__main__':
    main()
