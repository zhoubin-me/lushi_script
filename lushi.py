# -*- coding: utf-8 -*-
import pyautogui
import cv2
import time
import numpy as np

import os
import yaml

from types import SimpleNamespace
from PIL import ImageGrab, Image
import platform
import argparse
# import pytesseract

if platform.system() == 'Windows':
    import win32gui
    from winguiauto import findTopWindow

    def find_lushi_window(title):
        hwnd = findTopWindow(title)
        rect = win32gui.GetWindowPlacement(hwnd)[-1]
        image = ImageGrab.grab(rect)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        return rect, image
# elif platform.system() == 'Darwin':
#     import psutil
#     from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
#
#     def find_lushi_window(title):
#         for p in psutil.process_iter():
#             if p.name == title:
#                 pid = p.pid
#                 app = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
#                 app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
#         else:
#             raise ValueError("Hearthstone is not running")
else:
    raise ValueError(f"Plafform {platform.platform()} is not supported yet")


def find_icon_location(lushi, icon, confidence):
    result = cv2.matchTemplate(lushi, icon, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    if maxVal > confidence:
        (startX, startY) = maxLoc
        endX = startX + icon.shape[1]
        endY = startY + icon.shape[0]
        return True, (startX+endX)//2, (startY+endY)//2, maxVal
    else:
        return False, None, None, maxVal

def find_relative_loc(title='炉石传说'):
    pos = pyautogui.position()
    rect, _ = find_lushi_window(title)
    print((pos[0]-rect[0], pos[1]-rect[1]))


def move2loc(x, y, title='炉石传说'):
    rect, _ = find_lushi_window(title)
    loc = (x + rect[0], y + rect[1])
    pyautogui.moveTo(loc)


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
            img_folder = 'imgs_eng'
            self.title = 'hearthstone'
        elif self.lang == 'chs':
            cfg_file = 'config_chs.yaml'
            img_folder = "imgs_chs"
            self.title = "炉石传说"
        else:
            raise ValueError(f"Language {self.lang} is not supported yet")

        with open(cfg_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        self.basic = SimpleNamespace(**config['basic'])
        self.skill = SimpleNamespace(**config['skill'])
        self.locs = SimpleNamespace(**config['location'])
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
        x1, y1, x2, y2 = self.locs.enemy_region
        img = screen[x1:x2, y1:y2]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(img_gray, 250, 255, 0)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
        img_copy = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        # print(stats)
        for i in range(1, num_labels):
            mask = labels == i
            if stats[i][-1] > 50:
                img_copy[:, :, 0][mask] = 255
                img_copy[:, :, 1][mask] = 255
                img_copy[:, :, 2][mask] = 255

        # img_data = pytesseract.image_to_boxes(img_copy, config='--oem 3 -c tessedit_char_whitelist={0123456789}')
        # Image.fromarray(img_copy)


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

    def run_pvp(self):
        self.basic.reward_count = 5
        while True:
            time.sleep(self.basic.delay + np.random.rand())
            states, rect, screen = self.check_state()
            print(states)

            if 'pvp' in states:
                pyautogui.click(states['pvp'][0])
                continue

            if 'pvp_team' in states:
                pyautogui.click(rect[0] + self.locs.team_select[0], rect[1] + self.locs.team_select[1])
                continue
            
            if 'pvp_ready' in states or 'member_not_ready' in states:
                print("Surrendering")
                pyautogui.click(rect[0]+self.locs.options[0], rect[1]+self.locs.options[1])
                time.sleep(self.basic.pvp_delay)
                if self.basic.fast_surrender:
                    pyautogui.click(rect[0]+self.locs.surrender[0], rect[1]+self.locs.surrender[1])
                else:
                    states, rect, screen = self.check_state()
                    if 'surrender' in states:
                        pyautogui.click(states['surrender'][0])
                for _ in range(5):
                    pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
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
                continue
            
            pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])

    def run_pve(self):
        side = None
        surprise_in_mid = False
        heros_alive = 0
        battle_round_count = 0
        while True:
            time.sleep(np.random.rand()+0.5)
            states, rect, screen = self.check_state()
            print(f"{states}, rect: {rect[:2]} surprise side: {side}, surprise in middle: {surprise_in_mid}, battle round count : {battle_round_count}, heros alive {heros_alive}")

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
                pyautogui.click(rect[0]+self.locs.options[0], rect[1]+self.locs.options[1])
                pyautogui.click(rect[0]+self.locs.surrender[0], rect[1]+self.locs.surrender[1])
                continue

            if 'member_not_ready' in states:
                print("Selecting heros")
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
                print("Selecting skills")
                pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
                pyautogui.click(rect[0]+self.locs.heros[0], rect[1]+self.locs.heros[-1])

                skills = self.skill.ids[(battle_round_count-1) % self.skill.cycle]
                targets = self.skill.targets[(battle_round_count-1) % self.skill.cycle]

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
                continue

            if ('destroy' in states or 'blue_portal' in states or 'boom' in states) and self.basic.early_stop:
                pyautogui.click(self.locs.view_team[0]+rect[0], self.locs.view_team[1]+rect[1])
                pyautogui.click(self.locs.give_up[0]+rect[0], self.locs.give_up[1]+rect[1])
                pyautogui.click(self.locs.give_up_cfm[0]+rect[0], self.locs.give_up_cfm[1]+rect[1])
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
                        pyautogui.click(rect[0] + self.locs.visitors_confirm[0], rect[1] + self.locs.visitors_confirm[1])
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
                    pyautogui.click(self.locs.view_team[0]+rect[0], self.locs.view_team[1]+rect[1])
                    pyautogui.click(self.locs.give_up[0]+rect[0], self.locs.give_up[1]+rect[1])
                    pyautogui.click(self.locs.give_up_cfm[0]+rect[0], self.locs.give_up_cfm[1]+rect[1])
                continue

            
            if 'goto' in states or 'show' in states or 'collect' in states or 'teleport' in states:
                pyautogui.click(rect[0]+self.locs.start_game[0], rect[1]+self.locs.start_game[1])
                continue

            if 'start_game' in states:
                pyautogui.click(rect[0]+self.locs.start_game[0], rect[1]+self.locs.start_game[1])
                battle_round_count = 0
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
                pyautogui.click(rect[0]+self.locs.final_confirm[0], rect[1]+self.locs.final_confirm[1])
                continue

            if 'map_not_ready' in states and 'final_boss' in states:
                pyautogui.moveTo(rect[0]+self.locs.final_boss[0], rect[1]+self.locs.final_boss[1])
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                time.sleep(self.basic.delay)
                states, rect, screen = self.check_state()
                if 'start_game' in states:
                    pyautogui.click(rect[0]+self.locs.start_game[0], rect[1]+self.locs.start_game[1])
                    continue

            if 'map_not_ready' in states:
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
                    pyautogui.moveTo(x+rect[0], y+rect[1])
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()

            pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])

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
