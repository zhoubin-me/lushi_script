import pyautogui
import cv2
import time
import numpy as np

import win32gui
import os
import yaml

from types import SimpleNamespace
from PIL import ImageGrab, Image
from winguiauto import findTopWindow


def find_lushi_window():
    hwnd = findTopWindow("炉石传说")
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
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

    def load_config(self):
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        self.basic = SimpleNamespace(**config['basic'])
        self.skill = SimpleNamespace(**config['skill'])
        self.locs = SimpleNamespace(**config['location'])
        pyautogui.PAUSE = self.basic.delay
    
    def check_state(self):
        lushi, image = find_lushi_window()
        output_list = {}
        for k, v in self.icons.items():
            success, click_loc, conf = self.find_icon_loc(v, lushi, image)
            if success:
                output_list[k] = (click_loc, conf)
        return output_list, lushi
        
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
            states, rect = self.check_state()
            if 'surprise' in states:
                loc = states['surprise'][0]
                print(f"Found surprise at start {loc}")
                return loc
            if 'start_point' in states:
                break

        for _ in range(10):
            states, rect = self.check_state()
            pyautogui.scroll(40)
            if 'surprise' in states:
                for _ in range(10):
                    pyautogui.scroll(-40)
                loc = states['surprise'][0]
                print(f"Found surprise during scrolling {loc}")
                return loc
        
        print("Did not found any surprise")
        return None
    
    def enter_battle_mode(self):
        print("Entering battle mode")
        battle_round_count = 0
        while True:
            states, rect = self.check_state()
            time.sleep(np.random.rand()+self.basic.delay)
            if 'boom2' in states or 'ice_berg2' in states:
                print("Surrendering")
                pyautogui.click(rect[0]+self.locs.options[0], rect[1]+self.locs.options[1])
                pyautogui.click(rect[0]+self.locs.surrender[0], rect[1]+self.locs.surrender[1])
                break
            
            if 'member_ready' in states:
                print("Selecting heros")
                if self.basic.hero_count > 3:
                    first_x, last_x, y = self.locs.members
                    for i, idx in enumerate(self.basic.heros_id):
                        assert(self.basic.hero_count - i - 1 > 0)
                        dis = (last_x - first_x) // (self.basic.hero_count - i - 1)
                        loc = (first_x + dis * (idx - i), y)
                        pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                        pyautogui.moveTo(rect[0] + self.locs.dragto[0], rect[1] + self.locs.dragto[1])
                        pyautogui.click()
                continue

            if 'not_ready_dots' in states:
                print("Selecting skills")
                pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])
                pyautogui.click(rect[0]+self.locs.heros[0], rect[1]+self.locs.heros[-1])

                skills = self.skill.ids[battle_round_count % self.skill.cycle]
                targets = self.skill.targets[battle_round_count % self.skill.cycle]

                for idx, skill_id, target_id in zip([0, 1, 2], skills, targets):
                    hero_loc = (rect[0] + self.locs.heros[idx], rect[1] + self.locs.heros[-1])
                    skill_loc = (rect[0] + self.locs.skills[skill_id], rect[1] + self.locs.skills[-1])

                    pyautogui.moveTo(skill_loc)
                    pyautogui.click()
                    
                    if target_id != -1:
                        enemy_loc = (rect[0] + self.locs.enemies[1], rect[1] + self.locs.enemies[-1])
                        pyautogui.moveTo(enemy_loc)
                        pyautogui.click()
                
                pyautogui.moveTo(rect[0] + self.locs.start_battle[0], rect[1] + self.locs.start_battle[1])
                pyautogui.click()
                battle_round_count += 1
                continue

            if 'battle_ready' in states:
                pyautogui.click(states['battle_ready'][0])
                continue

            if 'final_reward' in states or 'final_reward2' in states:
                break

            if 'treasure_list' in states or 'treasure_replace' in states:
                treasure_id = np.random.randint(0, 3)
                treasure_loc = (self.locs.treasures[treasure_id], self.locs.treasures[-1])

                if 'ice_berg' in states:
                    x_dis = np.abs(treasure_loc[0] + rect[0] - states['ice_berg'][0][0])
                    if x_dis < 100:
                        continue
                
                if 'ancient_call' in states:
                    x_dis = np.abs(treasure_loc[0] + rect[0] - states['ancient_call'][0][0])
                    if x_dis < 100:
                        continue
                
                pyautogui.click(rect[0] + treasure_loc[0], rect[1] + treasure_loc[1])
                pyautogui.click(rect[0] + self.locs.treasures_collect[0], rect[1] + self.locs.treasures_collect[1])
                break

            pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])

        print("Battle ends")

    def run(self):
        side = None
        surprise_in_mid = False
        while True:
            time.sleep(np.random.rand()+0.5)
            states, rect = self.check_state()
            print(f"{states}, surprise side: {side}, surprise in middle: {surprise_in_mid}")

            if 'mercenaries' in states:
                pyautogui.click(states['mercenaries'][0])
                continue

            if 'travel' in states:
                pyautogui.click(states['travel'][0])
                pyautogui.click(rect[0] + self.locs.travel[0], rect[1] + self.locs.travel[1])
                continue

            if 'boss_list' in states:
                x_id = self.basic.boss_id % 3
                y_id = self.basic.boss_id // 3
                loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])
                print(x_id, y_id, loc)
                pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                pyautogui.click(rect[0] + self.locs.start_game[0], rect[1] + self.locs.start_game[1])
                continue

            if 'team_list' in states:
                x_id = self.basic.team_id % 3
                y_id = self.basic.team_id // 3
                pyautogui.click(rect[0] + self.locs.teams[x_id], rect[1] + self.locs.teams[3 + y_id])
                if 'team_lock' in states:
                    pyautogui.click(states['team_lock'][0])
                pyautogui.click(rect[0] + self.locs.team_select[0], rect[1] + self.locs.team_select[1])
                surprise_loc = self.scan_surprise_loc(rect)
                if surprise_loc is not None:
                    if  surprise_loc[0] < self.locs.start_point[0] + rect[0]:
                        side = 'left'
                    else:
                        side = 'right'
                    first_x, mid_x, last_x, y = self.locs.focus
                    if np.abs(surprise_loc[0] - rect[0] - mid_x) < 50:
                        surprise_in_mid = True
                    else:
                        surprise_in_mid = False
                    continue


            if 'visitor_list' in states:
                visitor_id = np.random.randint(0, 3)
                visitor_loc = (self.locs.visitors[visitor_id], self.locs.visitors[-1])
                pyautogui.click(rect[0] + visitor_loc[0], rect[1] + visitor_loc[1])
                pyautogui.click(rect[0] + self.locs.visitors_confirm[0], rect[1] + self.locs.visitors_confirm[1])
                if self.basic.early_stop:
                    pyautogui.click(self.locs.view_team[0]+rect[0], self.locs.view_team[1]+rect[1])
                    pyautogui.click(self.locs.give_up[0]+rect[0], self.locs.give_up[1]+rect[1])
                    pyautogui.click(self.locs.give_up_cfm[0]+rect[0], self.locs.give_up_cfm[1]+rect[1])
                continue

            
            if 'goto' in states or 'show' in states or 'collect' in states or 'teleport' in states:
                pyautogui.click(rect[0]+self.locs.start_game[0], rect[1]+self.locs.start_game[1])
                continue

            if 'start_game' in states:
                pyautogui.click(rect[0]+self.locs.start_game[0], rect[1]+self.locs.start_game[1])
                self.enter_battle_mode()
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
                
                if 'surprise' in states:
                    surprise_loc = states['surprise'][0]
                    if (side == 'left' and first_x < surprise_loc[0] and surprise_loc[0] < mid_x) or (side == 'right' and mid_x < surprise_loc[0] and surprise_loc[0] < last_x):
                        if np.abs(surprise_loc[1] - rect[1] - self.locs.focus[-1]) < 100:
                            pyautogui.moveTo(surprise_loc)
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                            time.sleep(0.5)
                            states, rect = self.check_state()
                            if  ('destroy' in states or 'blue_portal' in states or 'boom' in states) and self.basic.early_stop:
                                pyautogui.click(self.locs.view_team[0]+rect[0], self.locs.view_team[1]+rect[1])
                                pyautogui.click(self.locs.give_up[0]+rect[0], self.locs.give_up[1]+rect[1])
                                pyautogui.click(self.locs.give_up_cfm[0]+rect[0], self.locs.give_up_cfm[1]+rect[1])
                                continue
                            
                            if 'goto' in states or 'show' in states or 'collect' in states or 'teleport' in states:
                                pyautogui.click(rect[0]+self.locs.start_game[0], rect[1]+self.locs.start_game[1])
                                continue
            
                for x in (x1, x2, x3):
                    pyautogui.moveTo(x+rect[0], y+rect[1])
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                
                time.sleep(0.5)
                states, rect = self.check_state()

                if 'map_not_ready' in states and 'final_boss' in states:
                    pyautogui.moveTo(rect[0]+self.locs.final_boss[0], rect[1]+self.locs.final_boss[1])
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()

            pyautogui.click(rect[0] + self.locs.empty[0], rect[1] + self.locs.empty[1])




def main():
    info = '''
        Please start Hearthstone, change to windows mode, resolution to 1600x900, high quality graphics; 
        Currently only support 3 heros on battle field, please make sure you heros won't die, otherwise may cause problems; 
        Please refer to config.yaml to modify your configurations
        '''

    pyautogui.confirm(text=info)
    agent = Agent()
    agent.run()
            

if __name__ == '__main__':
    main()
