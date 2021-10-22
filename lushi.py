import pyautogui
import cv2
import time
from PIL import ImageGrab, Image
import numpy as np

import win32api
from winguiauto import findTopWindow
import win32gui
import win32con



class Icons:
    def __init__(self):
        for k, v in Images.__dict__.items():
            if not k.startswith('_'):
                setattr(self, k, self.fname2img(v))

    @staticmethod
    def fname2img(fname):
        return cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2GRAY)


def find_lushi_window():
    hwnd = findTopWindow("炉石传说")
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    return rect, image

def find_icon_location(lushi, icon):
    result = cv2.matchTemplate(lushi, icon, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    if maxVal > 0.8:
        (startX, startY) = maxLoc
        endX = startX + icon.shape[1]
        endY = startY + icon.shape[0]
        return True, (startX+endX)//2, (startY+endY)//2, maxVal
    else:
        return False, None, None, maxVal

    
class Images:
    yongbing = 'imgs/yongbing.png'
    travel = 'imgs/travel.png'
    air_element = 'imgs/air.png'
    team_list = 'imgs/team_list.png'
    team_lock = 'imgs/team_lock.png'
    start_point = 'imgs/start_point.png'

    member_ready = 'imgs/member_ready.png'

    not_ready = 'imgs/not_ready.png'
    skill_select = 'imgs/skill_select.png'
    battle_ready2 = 'imgs/battle_ready2.png'
    surprise = 'imgs/surprise2.png'

    treasure_list = 'imgs/treasure_list.png'
    treasure_replace = 'imgs/treasure_replace.png'
    visitor_list = 'imgs/visitor_list.png'
    final_reward = 'imgs/final_reward.png'

    final_confirm = 'imgs/final_confirm.png'
    boom = 'imgs/boom.png'

class Agent:
    def __init__(self, team_id, heros_id, skills_id, targets_id, hero_cnt):
        self.icons = Icons()
        self.team_id = team_id
        self.heros_id = heros_id
        self.skills_id = skills_id
        self.targets_id = targets_id
        self.hero_cnt = hero_cnt

        self.hero_relative_locs = [
            (677, 632),
            (807, 641),
            (943, 641)
        ]

        self.enemy_mid_location = (850, 285)

        self.skill_relative_locs = [
            (653, 447),
            (801, 453),
            (963, 459),
        ]

        self.treasure_locs = [
            (707, 488), (959, 462), (1204, 474)
        ]
        self.treasure_collect_loc = (968, 765)

        self.visitor_locs = [
            (544, 426), (790, 420), (1042, 416)
        ]
        self.visitor_choose_loc = (791, 688)

        self.members_loc = (622, 1000, 900)

        self.drag2loc = (1213, 564)

        self.locs = {
            'left': [(452, 464), (558, 461), (473, 465)],
            'right': [(777, 478), (800, 459), (903, 469)]
        }

        self.finial_reward_locs = [
            (660, 314), (554, 687), (1010, 794), (1117, 405), (806, 525)
        ]

        self.select_travel_relative_loc = (1090, 674)

        self.team_locations = [(374, 324), (604, 330), (837, 324)]
        self.team_loc = self.team_locations[team_id]
        self.start_team_loc = (1190, 797)
        self.start_game_relative_loc = (1250, 732)
        self.start_point_relative_loc = (646, 712)

        self.options_loc = (1579, 920)
        self.surrender_loc = (815, 363)

        self.empty_loc = (1518, 921)

    
    def run(self):
        surprise_loc = None
        while True:
            time.sleep(np.random.rand()+0.5)
            states, rect = self.check_state()
            pyautogui.moveTo(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
            pyautogui.click()
            print(states)

            if 'yongbing' in states:
                pyautogui.click(states['yongbing'][0])
                continue

            if 'travel' in states:
                pyautogui.click(states['travel'][0])
                pyautogui.click(rect[0] + self.select_travel_relative_loc[0], rect[1] + self.select_travel_relative_loc[1])
                continue

            if 'air_element' in states:
                pyautogui.click(states['air_element'][0])
                pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
                continue
            
            if 'team_list' in states:
                pyautogui.click(rect[0] + self.team_loc[0], rect[1] + self.team_loc[1])
                if 'team_lock' in states:
                    pyautogui.click(states['team_lock'][0])
                pyautogui.click(rect[0] + self.start_team_loc[0], rect[1] + self.start_team_loc[1])
                continue

            if 'member_ready' in states:
                if 'boom' in states:
                    print("Surrendering")
                    pyautogui.click(rect[0]+self.options_loc[0], rect[1]+self.options_loc[1])
                    pyautogui.click(rect[0]+self.surrender_loc[0], rect[1]+self.surrender_loc[1])
                    continue
                
                first_x, last_x, y = self.members_loc
                for i, idx in enumerate(self.heros_id):
                    assert(self.hero_cnt - i - 1 > 0)
                    dis = (last_x - first_x) // (self.hero_cnt - i - 1)
                    loc = (first_x + dis * (idx - i), y)
                    pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                    pyautogui.click(rect[0] + self.drag2loc[0], rect[1] + self.drag2loc[1])
                
                pyautogui.click(states['member_ready'][0])
                continue

            if 'battle_ready2' in states:
                pyautogui.click(states['battle_ready2'][0])
                continue


            if 'treasure_list' in states or 'treasure_replace' in states:
                treasure_loc_id = np.random.randint(0, 3)
                treasure_loc = self.treasure_locs[treasure_loc_id]
                pyautogui.click(rect[0] + treasure_loc[0], rect[1] + treasure_loc[1])
                pyautogui.click(rect[0] + self.treasure_collect_loc[0], rect[1] + self.treasure_collect_loc[1])
                continue     
                

            if 'visitor_list' in states:
                visitor_id = np.random.randint(0, 3)
                visitor_loc = self.visitor_locs[visitor_id]
                pyautogui.click(rect[0] + visitor_loc[0], rect[1] + visitor_loc[1])
                pyautogui.click(rect[0] + self.visitor_choose_loc[0], rect[1] + self.visitor_choose_loc[1])
                continue
            
            if 'final_reward' in states:
                for rew in self.finial_reward_locs:
                    pyautogui.moveTo(rect[0]+rew[0], rect[1]+rew[1])
                    pyautogui.click()
                continue

            if 'final_confirm' in states:
                pyautogui.click(states['final_confirm'][0])
                surprise_loc = None
                continue
            
            if 'start_game' in states:
                pyautogui.click(states['start_game'][0])
                continue

            if 'surprise' in states:
                surprise_loc = states['surprise'][0]
                if 'start_point' not in states:
                    if  surprise_loc[0] < self.start_point_relative_loc[0] + rect[0]:
                        side = 'left'
                    else:
                        side = 'right'
                    side_locs = self.locs[side]
                    for loc in side_locs:
                        pyautogui.moveTo(loc[0] + rect[0], loc[1] + rect[1])
                        pyautogui.click(clicks=2, interval=0.25)
                    pyautogui.click(surprise_loc)
                continue
            
            if 'skill_select' in states or 'not_ready' in states:
                pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
                first_hero_loc = self.hero_relative_locs[0]
                pyautogui.click(rect[0]+first_hero_loc[0], rect[1]+first_hero_loc[1])

                for idx, skill_id, target_id in zip([0, 1, 2], self.skills_id, self.targets_id):
                    hero_loc = (rect[0] + self.hero_relative_locs[idx][0], rect[1] + self.hero_relative_locs[idx][1])
                    skill_loc = (rect[0] + self.skill_relative_locs[skill_id][0], rect[1] + self.skill_relative_locs[skill_id][1])
                    pyautogui.click(*skill_loc)
                    
                    if target_id != -1:
                        enemy_loc = (rect[0] + self.enemy_mid_location[0], rect[1] + self.enemy_mid_location[1])
                        pyautogui.click(*enemy_loc)
                continue



    def check_state(self):
        lushi, image = find_lushi_window()
        output_list = {}
        for k, v in self.icons.__dict__.items():
            if not k.startswith('_'):
                success, click_loc, conf = self.find_icon_and_click_loc(v, lushi, image)
                if success:
                    output_list[k] = (click_loc, conf)
        return output_list, lushi
        
    def find_icon_and_click_loc(self, icon, lushi, image):
        success, X, Y, conf = find_icon_location(image, icon)
        if success:
            click_loc = (X + lushi[0], Y + lushi[1])
        else:
            click_loc = None
        return success, click_loc, conf

def find_relative_loc():
    pos = pyautogui.position()
    rect, _ = find_lushi_window()
    print((pos[0]-rect[0], pos[1]-rect[1]))


def move2loc(x, y):
    pos = pyautogui.position()
    rect, _ = find_lushi_window()
    loc = (x + rect[0], y + rect[1])
    pyautogui.moveTo(loc)

def main():
    pyautogui.PAUSE = 0.8
    pyautogui.confirm(text="请启动炉石，将炉石调至窗口模式，分辨率设为1600x900，画质设为高; 程序目前只支持三个场上英雄，请确保上场英雄不会死且队伍满6人，否则脚本会出错；请参考config.txt修改配置文件")
    with open('config.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    assert(len(lines) == 4)

    team_id, heros_id, skills_id, targets_id = lines


    heros_id = [int(s.strip()) for s in heros_id.strip().split(' ') if not s.startswith('#')]
    skills_id = [int(s.strip()) for s in skills_id.strip().split(' ') if not s.startswith('#')]
    targets_id = [int(s.strip()) for s in targets_id.strip().split(' ') if not s.startswith('#')]
    team_id, hero_cnt = [int(s.strip()) for s in team_id.strip().split(' ') if not s.startswith('#')]

    assert(len(skills_id) == 3 and len(targets_id) == 3 and len(heros_id) == 3)
    assert(team_id in [0, 1, 2] and hero_cnt <= 6)


    agent = Agent(team_id=team_id, heros_id=heros_id, skills_id=skills_id, targets_id=targets_id, hero_cnt=hero_cnt)
    agent.run()
            

if __name__ == '__main__':
    main()
