import pyautogui
import cv2
import time
from PIL import ImageGrab, Image
import numpy as np

import win32api
from winguiauto import findTopWindow
import win32gui
import win32con
import os




def find_lushi_window():
    hwnd = findTopWindow("炉石传说")
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
    image.save('out.png')
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    return rect, image

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


def find_relative_loc():
    pos = pyautogui.position()
    rect, _ = find_lushi_window()
    print((pos[0]-rect[0], pos[1]-rect[1]))


def move2loc(x, y):
    rect, _ = find_lushi_window()
    loc = (x + rect[0], y + rect[1])
    pyautogui.moveTo(loc)


class Agent:
    def __init__(self):
        self.icons = {}
        imgs = [img for img in os.listdir('imgs') if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join('imgs', img)), cv2.COLOR_BGR2GRAY)
            self.icons[k] = v
        
        self.load_config()

        self.hero_relative_locs = [
            (677, 632),
            (807, 641),
            (943, 641)
        ]

        self.boss_relative_locs = [
            (405, 352),
            (676, 345),
            (916, 362),
            (405, 667),
            (676, 667),
            (916, 667),
        ]

        self.enemy_mid_location = (850, 285)

        self.skill_relative_locs = [
            (653, 447),
            (801, 453),
            (963, 459),
        ]

        self.treasure_locs = [
            (707, 376), (959, 376), (1204, 376)
        ]
        self.treasure_collect_loc = (968, 765)

        self.visitor_locs = [
            (544, 426), (790, 420), (1042, 416)
        ]
        self.visitor_choose_loc = (791, 688)

        self.members_loc = (622, 1000, 900)

        self.drag2loc = (1213, 564)

        self.map_locs = (420, 650, 900, 453)

        reward_locs = {
            5: [(608, 706), (1034, 720), (1117, 371), (846, 311), (541, 430), (806, 525)],
            4: [(660, 314), (554, 687), (1010, 794), (1117, 405), (806, 525)],
            3: [(608, 706), (1034, 720), (1117, 371), (846, 311), (541, 430), (806, 525)],
        }

        self.final_reward_locs = reward_locs[self.reward_cnt]

        self.select_travel_relative_loc = (1090, 674)

        self.team_locations = [(374, 324), (604, 330), (837, 324)]
        self.team_loc = self.team_locations[self.team_id]
        self.start_team_loc = (1190, 797)
        self.start_game_relative_loc = (1250, 732)
        self.start_point_relative_loc = (646, 712)

        self.options_loc = (1579, 920)
        self.surrender_loc = (815, 363)

        self.start_battle_loc = (1327, 454)
        self.check_team_loc = (674, 885)
        self.give_up_loc = (929, 706)
        self.give_up_cfm_loc = (712, 560)
        self.empty_loc = (1488, 921)
        self.final_confirm = (794, 779)
        self.final_boss_loc = (646, 227)

    def load_config(self):
        with open('config.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        others, heros_id, skills_id, targets_id, early_stop, delay, confidence = lines
        self.heros_id = [int(s.strip()) for s in heros_id.strip().split(' ') if not s.startswith('#')]
        self.skills_id = [int(s.strip()) for s in skills_id.strip().split(' ') if not s.startswith('#')]
        self.targets_id = [int(s.strip()) for s in targets_id.strip().split(' ') if not s.startswith('#')]

        self.team_id, self.hero_cnt, self.boss_id, self.reward_cnt = [int(s.strip()) for s in others.strip().split(' ') if not s.startswith('#')]

        self.early_stop = int(early_stop.split('#')[0].strip())
        self.confidence = float(confidence.split('#')[0].strip())

        assert(len(self.skills_id) == 3 and len(self.targets_id) == 3 and len(self.heros_id) == 3)
        assert(self.team_id in [0, 1, 2] and self.hero_cnt <= 6 and self.boss_id in list(range(6)))

        pyautogui.PAUSE = float(delay.split('#')[0].strip())
    
    def check_state(self):
        lushi, image = find_lushi_window()
        output_list = {}
        for k, v in self.icons.items():
            success, click_loc, conf = self.find_icon_loc(v, lushi, image)
            if success:
                output_list[k] = (click_loc, conf)
        return output_list, lushi
        
    def find_icon_loc(self, icon, lushi, image):
        success, X, Y, conf = find_icon_location(image, icon, self.confidence)
        if success:
            click_loc = (X + lushi[0], Y + lushi[1])
        else:
            click_loc = None
        return success, click_loc, conf

    def run(self):
        side = None
        surprise_loc = None
        while True:
            time.sleep(np.random.rand()+0.5)
            states, rect = self.check_state()
            print(states, self.early_stop)

            if  ('destroy' in states or 'blue_portal' in states or 'boom' in states) and self.early_stop:
                pyautogui.click(self.check_team_loc[0]+rect[0], self.check_team_loc[1]+rect[1])
                pyautogui.click(self.give_up_loc[0]+rect[0], self.give_up_loc[1]+rect[1])
                pyautogui.click(self.give_up_cfm_loc[0]+rect[0], self.give_up_cfm_loc[1]+rect[1])
                continue
            
            if 'visitor_list' in states:
                visitor_id = np.random.randint(0, 3)
                visitor_loc = self.visitor_locs[visitor_id]
                pyautogui.click(rect[0] + visitor_loc[0], rect[1] + visitor_loc[1])
                pyautogui.click(rect[0] + self.visitor_choose_loc[0], rect[1] + self.visitor_choose_loc[1])
                if self.early_stop:
                    pyautogui.click(self.check_team_loc[0]+rect[0], self.check_team_loc[1]+rect[1])
                    pyautogui.click(self.give_up_loc[0]+rect[0], self.give_up_loc[1]+rect[1])
                    pyautogui.click(self.give_up_cfm_loc[0]+rect[0], self.give_up_cfm_loc[1]+rect[1])
                continue

            if 'treasure_list' in states or 'treasure_replace' in states:
                treasure_loc_id = np.random.randint(0, 3)
                treasure_loc = self.treasure_locs[treasure_loc_id]

                if 'ice_berg' in states:
                    x_dis = np.abs(treasure_loc[0] + rect[0] - states['ice_berg'][0][0])
                    if x_dis < 100:
                        continue
                
                if 'ancient_call' in states:
                    x_dis = np.abs(treasure_loc[0] + rect[0] - states['ancient_call'][0][0])
                    if x_dis < 100:
                        continue
                
                pyautogui.click(rect[0] + treasure_loc[0], rect[1] + treasure_loc[1])
                pyautogui.click(rect[0] + self.treasure_collect_loc[0], rect[1] + self.treasure_collect_loc[1])
                continue

            if 'mercenaries' in states:
                pyautogui.click(states['mercenaries'][0])
                continue

            if 'travel' in states:
                pyautogui.click(states['travel'][0])
                pyautogui.click(rect[0] + self.select_travel_relative_loc[0], rect[1] + self.select_travel_relative_loc[1])
                continue

            if 'boss_list' in states:
                loc = self.boss_relative_locs[self.boss_id]
                pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
                continue
            
            if 'final_reward' in states or 'final_reward2' in states:
                for loc in self.final_reward_locs:
                    pyautogui.moveTo(rect[0] + loc[0], rect[1] + loc[1])
                    pyautogui.click()
                continue

            if 'final_confirm' in states:
                pyautogui.click(rect[0]+self.final_confirm[0], rect[1]+self.final_confirm[1])
                continue
            
            if 'team_list' in states:
                pyautogui.click(rect[0] + self.team_loc[0], rect[1] + self.team_loc[1])
                if 'team_lock' in states:
                    pyautogui.click(states['team_lock'][0])
                pyautogui.click(rect[0] + self.start_team_loc[0], rect[1] + self.start_team_loc[1])
                continue

            if 'member_ready' in states:
                if 'boom2' in states or 'ice_berg2' in states:
                    print("Surrendering")
                    pyautogui.click(rect[0]+self.options_loc[0], rect[1]+self.options_loc[1])
                    pyautogui.click(rect[0]+self.surrender_loc[0], rect[1]+self.surrender_loc[1])
                    continue

                if self.hero_cnt > 3:
                    first_x, last_x, y = self.members_loc
                    for i, idx in enumerate(self.heros_id):
                        assert(self.hero_cnt - i - 1 > 0)
                        dis = (last_x - first_x) // (self.hero_cnt - i - 1)
                        loc = (first_x + dis * (idx - i), y)
                        pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                        pyautogui.moveTo(rect[0] + self.drag2loc[0], rect[1] + self.drag2loc[1])
                        pyautogui.click()
                pyautogui.click(states['member_ready'][0])
                continue

            if 'battle_ready' in states:
                pyautogui.click(rect[0] + self.start_battle_loc[0], rect[1] + self.start_battle_loc[1])
                continue

            if 'not_ready_dots' in states:
                pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
                first_hero_loc = self.hero_relative_locs[0]
                pyautogui.click(rect[0]+first_hero_loc[0], rect[1]+first_hero_loc[1])

                for idx, skill_id, target_id in zip([0, 1, 2], self.skills_id, self.targets_id):
                    hero_loc = (rect[0] + self.hero_relative_locs[idx][0], rect[1] + self.hero_relative_locs[idx][1])
                    skill_loc = (rect[0] + self.skill_relative_locs[skill_id][0], rect[1] + self.skill_relative_locs[skill_id][1])

                    pyautogui.moveTo(skill_loc)
                    pyautogui.click()
                    
                    if target_id != -1:
                        enemy_loc = (rect[0] + self.enemy_mid_location[0], rect[1] + self.enemy_mid_location[1])
                        pyautogui.moveTo(enemy_loc)
                        pyautogui.click()
                pyautogui.moveTo(rect[0] + self.start_battle_loc[0], rect[1] + self.start_battle_loc[1])
                pyautogui.click()
                continue

            if 'start_game' in states or 'stranger' in states or 'goto' in states or 'show' in states or 'collect' in states or 'teleport' in states:
                pyautogui.click(rect[0]+self.start_game_relative_loc[0], rect[1]+self.start_game_relative_loc[1])
                continue

            if 'surprise' in states:
                surprise_loc = states['surprise'][0]
                if  surprise_loc[0] < self.start_point_relative_loc[0] + rect[0]:
                    side = 'left'
                else:
                    side = 'right'

            if 'map_not_ready' in states:
                first_x, mid_x, last_x, y = self.map_locs
                if side is None:
                    side = 'left'
                if side == 'left':
                    x1, x2, x3 = first_x, (first_x + mid_x) // 2, mid_x
                else:
                    x1, x2, x3 = mid_x, (last_x + mid_x) // 2, last_x

                for x in (x1, x2, x3):
                    pyautogui.moveTo(x+rect[0], y+rect[1])
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()

                if 'surprise' in states:
                    surprise_loc = states['surprise'][0]
                    if (side == 'left' and first_x < surprise_loc[0] and surprise_loc[0] < mid_x) or (side == 'right' and mid_x < surprise_loc[0] and surprise_loc[0] < last_x):
                        if np.abs(surprise_loc[1] - rect[1] - self.map_locs[-1]) < 100:
                            pyautogui.moveTo(surprise_loc, duration=0.5)
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                
            pyautogui.click(rect[0] + self.empty_loc[0], rect[1] + self.empty_loc[1])

def main():
    pyautogui.confirm(text="请启动炉石，将炉石调至窗口模式，分辨率设为1600x900，画质设为高，语言设为简体中文; 程序目前只支持三个场上英雄，请确保上场英雄不会死且队伍满6人，否则脚本可能会出错；请参考config.txt修改配置文件")
    agent = Agent()
    agent.run()
            

if __name__ == '__main__':
    main()
