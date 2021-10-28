# -*- coding: utf-8 -*-
import pyautogui
import cv2
import time
import numpy as np
import argparse
import os
import yaml
from types import SimpleNamespace

from util import find_lushi_window, find_icon_location, restart_game, set_top_window


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
        self.skill = SimpleNamespace(**config['skill'])
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

    def check_state(self):
        lushi, image = find_lushi_window(self.title)
        output = {}
        for k, v in self.icons.items():
            success, click_loc, conf = self.find_icon_loc(v, lushi, image)
            if success:
                output[k] = (click_loc, conf)

        for k, v in self.treasure_blacklist.items():
            success, click_loc, conf = self.find_icon_loc(v, lushi, image)
            if success:
                output[k] = (click_loc, conf)

        for k, v in self.heros_whitelist.items():
            success, click_loc, conf = self.find_icon_loc(v, lushi, image)
            if success:
                output[k] = (click_loc, conf)

        return output, lushi, image

    def analyse_battle_field(self, screen):
        pass
    
    def find_icon_loc(self, icon, lushi, image):
        success, X, Y, conf = find_icon_location(image, icon, self.basic.confidence)
        if success:
            click_loc = (X + lushi[0], Y + lushi[1])
        else:
            click_loc = None
        return success, click_loc, conf

    def scan_surprise_loc(self, rect):
        print('Scanning surprise')
        pyautogui.moveTo(rect[0] + self.locs.scroll[0], rect[1] + self.locs.scroll[1])
        while True:
            states, rect, screen = self.check_state()
            if 'surprise' in states:
                loc = states['surprise'][0]
                print(f"Found surprise at start {loc}")
                return loc
            if 'start_point' in states:
                break

        for _ in range(10):
            states, rect, screen = self.check_state()
            pyautogui.scroll(60)
            if 'surprise' in states:
                for _ in range(10):
                    pyautogui.scroll(-60)
                loc = states['surprise'][0]
                print(f"Found surprise during scrolling {loc}")
                return loc

        print("Did not found any surprise")
        return None

    def analyse_battle_field(self, region, screen):
        x1, y1, x2, y2 = region
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        img = screen[y1:y2, x1:x2]
        digits = cv2.imread('digits.png')
        cv2.imwrite('gray.png', img)
        _, thresh1 = cv2.threshold(img[:, :, 2], 250, 255, 0)
        _, thresh2 = cv2.threshold(img[:, :, 1], 250, 255, 0)
        thresh = cv2.bitwise_or(thresh1, thresh2)
        cv2.imwrite('gray_thr.png', thresh)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
        img_copy = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        data = []
        print(stats)
        for i in range(1, num_labels):
            mask = labels == i
            x, y, w, h, a = stats[i]
            w, h = 17, 30
            if stats[i][-1] > 100:
                if x < 3 or y < 3:
                    continue
                img_copy[:, :, 0][mask] = 255
                img_copy[:, :, 1][mask] = 255
                img_copy[:, :, 2][mask] = 255
                digit = img_copy[y - 3:y + h, x - 3:x + w]
                cv2.imwrite(f'digit_{i}.png', digit)
                success, x, y, conf = find_icon_location(digits, digit, 0.7)
                data.append(list(stats[i][:-1]) + [conf, np.rint((x - 14) / 28)])
                print(i, data[-1])
        cv2.imwrite('gray_copy.png', img_copy)
        data.sort(key=lambda e: e[0])
        data_clean = []
        for i, entry in enumerate(data):
            if i == 0:
                data_clean.append(entry)
            else:
                x_diff = entry[0] - data_clean[-1][0]
                if np.abs(x_diff) < 30:
                    data_clean[-1][2] = x_diff + entry[2]
                    data_clean[-1][-1] = data_clean[-1][-1] * 10 + entry[-1]
                else:
                    data_clean.append(entry)
        assert (len(data_clean) % 2 == 0)
        N = len(data_clean) // 2
        output = {}
        for i in range(N):
            damage, health = data_clean[2 * i], data_clean[2 * i + 1]
            center_x = (damage[0] + damage[2] // 2 + health[0] + health[2] // 2) // 2
            center_y = (damage[1] + damage[3]) // 2 + 28
            color_region = img[center_y - 5:center_y + 5, center_x - 10:center_x + 10]
            cv2.imwrite(f'color_{i}.png', color_region)
            B, G, R = color_region.mean(axis=0).mean(axis=0).astype(np.int32)
            maximum = max(B, G, R)
            if maximum > 100:
                if maximum == B:
                    color = 'b'
                elif maximum == G:
                    color = 'g'
                else:
                    color = 'r'
            else:
                color = 'n'

            hero_x, hero_y = center_x + x1, center_y + y1 - 70
            output[i] = (hero_x, hero_y, int(damage[-1]), int(health[-1]), color)
            cv2.imwrite(f'hero_{i}.png', screen[hero_y - 35:hero_y + 35, hero_x - 50:hero_x + 50])
            print(B, G, R)
        print(output)
        return output

    def run_pvp(self):
        self.basic.reward_count = 5
        state = ""
        tic = time.time()
        while True:
            time.sleep(self.basic.delay + np.random.rand())
            states, rect, screen = self.check_state()
            print(states)

            if time.time() - tic > self.basic.longest_waiting:
                restart_game(self.lang, self.basic.battle_net_path)
                tic = time.time()
            if 'mercenaries' in states:
                pyautogui.click(states['mercenaries'][0])
                if state != "mercenaries":
                    state = "mercenaries"
                    tic = time.time()
                continue

            if 'pvp' in states:
                pyautogui.click(states['pvp'][0])
                if state != "pvp":
                    state = "pvp"
                    tic = time.time()
                continue

            if 'pvp_team' in states:
                tic = time.time()
                pyautogui.click(rect[0] + self.locs.team_select[0], rect[1] + self.locs.team_select[1])
                if state != "pvp_team":
                    state = "pvp_team"
                    tic = time.time()
                continue

            if 'pvp_ready' in states or 'member_not_ready' in states:
                print("Surrendering")
                pyautogui.click(rect[0] + self.locs.options[0], rect[1] + self.locs.options[1])
                time.sleep(self.basic.pvp_delay)
                if self.basic.fast_surrender:
                    pyautogui.click(rect[0] + self.locs.surrender[0], rect[1] + self.locs.surrender[1])
                else:
                    states, rect, screen = self.check_state()
                    if 'surrender' in states:
                        pyautogui.click(states['surrender'][0])
                for _ in range(5):
                    pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])

                if state != "pvp_ready":
                    state = "pvp_ready"
                    tic = time.time()
                continue

            if 'final_reward' in states or 'final_reward2' in states:
                reward_locs = eval(self.locs.rewards[self.basic.reward_count])
                for loc in reward_locs:
                    pyautogui.moveTo(rect[0] + loc[0], rect[1] + loc[1])
                    pyautogui.click()
                pyautogui.moveTo(rect[0] + self.locs.rewards['confirm'][0], rect[1] + self.locs.rewards['confirm'][1])
                pyautogui.click()
                for _ in range(5):
                    pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
                if state != "final_reward":
                    state = "final_reward"
                    tic = time.time()
                continue

            if state != "":
                state = ""
                tic = time.time()

            pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])

    def run_pve(self):
        side = None
        surprise_in_mid = False
        heros_alive = 0
        battle_round_count = 0
        skill_selection_retry = 0
        heroes_selection_retry = 0
        find_map_entry_retry = 0
        while True:
            time.sleep(np.random.rand() + self.basic.delay)
            states, rect, screen = self.check_state()
            print(
                f"{states}, rect: {rect[:2]} surprise side: {side}, surprise in middle: {surprise_in_mid}, battle round count : {battle_round_count}, heros alive {heros_alive}")

            if 'mercenaries' in states:
                pyautogui.click(states['mercenaries'][0])
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

            if 'summoned_demon' in states:
                # sometimes the opponent may summon an extra demon on their side or our side, check the coordinate
                # if it's on our side, surrender
                # this may not work if there's a demon on both sides
                print('Found Summoned Demon, checking coordinates', states)
                if states['summoned_demon'][0][1] > self.locs.resolution[1] / 2:  # if it's on enemy side
                    print("Surrendering due to extra minion on our side", states)
                    pyautogui.click(rect[0] + self.locs.options[0], rect[1] + self.locs.options[1])
                    pyautogui.click(rect[0] + self.locs.surrender[0], rect[1] + self.locs.surrender[1])
                continue

            if 'member_not_ready' in states:
                if heroes_selection_retry > self.retry.hero_selection:
                    print("Surrendering due to cannot select next hero", states)
                    pyautogui.click(rect[0] + self.locs.options[0], rect[1] + self.locs.options[1])
                    pyautogui.click(rect[0] + self.locs.surrender[0], rect[1] + self.locs.surrender[1])
                    continue

                print("Selecting heroes, attempt", heroes_selection_retry)
                heroes_selection_retry += 1
                first_x, last_x, y = self.locs.members
                mid_x = (first_x + last_x) // 2
                for i, idx in enumerate(self.basic.start_heros_id):
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
                if skill_selection_retry > self.retry.skill_selection:
                    print("Surrendering", states)
                    pyautogui.click(rect[0] + self.locs.options[0], rect[1] + self.locs.options[1])
                    pyautogui.click(rect[0] + self.locs.surrender[0], rect[1] + self.locs.surrender[1])
                    continue

                print("Selecting skills, attempt", skill_selection_retry)
                skill_selection_retry += 1
                pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
                pyautogui.click(rect[0] + self.locs.heros[0], rect[1] + self.locs.heros[-1])

                skills = self.skill.ids[(battle_round_count - 1) % self.skill.cycle]
                targets = self.skill.targets[(battle_round_count - 1) % self.skill.cycle]

                for idx, skill_id, target_id in zip([0, 1, 2], skills, targets):
                    hero_loc = (rect[0] + self.locs.heros[idx], rect[1] + self.locs.heros[-1])
                    skill_loc = (rect[0] + self.locs.skills[skill_id], rect[1] + self.locs.skills[-1])

                    pyautogui.moveTo(skill_loc)
                    pyautogui.click()

                    if target_id != -1:
                        enemy_loc = (rect[0] + self.locs.enemies[1], rect[1] + self.locs.enemies[-1])
                        pyautogui.moveTo(enemy_loc)
                        pyautogui.click()
                continue

            if 'battle_ready' in states:
                pyautogui.click(states['battle_ready'][0])
                battle_round_count += 1
                skill_selection_retry = 0
                heroes_selection_retry = 0
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

            # pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])

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
