# -*- coding: utf-8 -*-
import random
import time
from types import SimpleNamespace

import pyautogui

import lushi
import main_gui
import unittest
import os
import cv2
import numpy as np
import yaml
from utils.util import find_lushi_window, find_icon_location, restart_game, tuple_add, find_relative_loc


class TestLushi(unittest.TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self) -> None:
        return super().tearDown()

    def get_save_image(self, idx=0, to_gray=True):
        # 罗卡拉 英雄, 英雄列表， 宝藏列表， 香蕉英雄列表
        imageNames = ["reward_2021-11-15_05-23.png", "reward_2021-11-15_04-14.png", "reward_2021-11-15_20-28.png",
                      "reward_2021-11-15_10-20.png", "treasure[0,1,2]_17-19.59,312.png", "treasure[0,1]_18-35.41,966.png",
                      "treasure[xx]_09-54.35,566.png", "visitor_list_10-20.33,562.png"]
        imgPath = os.path.join(".", "resource", "imgs_eng_1024x768", "img", imageNames[idx])
        src = cv2.imread(imgPath)
        if to_gray:
            image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        else:
            image = np.array(src)
        return image

    def get_config(self, lang='eng'):
        config = {}

        try:
            with open(f'config/locs_{lang}.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except:
            return ""

        config['title'] = 'hearthstone'
        config['lang'] = 'eng'
        config['loc_file'] = 'config/locs_eng.yaml'
        config['img_folder'] = 'resource/imgs_eng_1024x768'
        config['screenshot_reward'] = True
        config['lang'] = 'EN-1024x768'
        config['treasure_blacklist'] = {}
        # config['lang'] = 'EN-1024x768'
        config['reward_count_dropdown'] = 3
        config['hero'] = {}
        config['hs_path'] = 'C:/Program Files (x86)/Hearthstone/Hearthstone.exe'
        config['delay'] = 0.5
        config['confidence'] = 0.8
        config['stop_at_boss'] = 0
        config['fix_x'] = 0 
        config['fix_y'] = 0
        config['lettuce_role_limit'] = 4
        config['map_decision'] = 0
        config['battle_time_wait'] = 1
        config['choice_skill_index'] = 2
        
        return config

    def test_treasure(self):
        config = self.get_config()
        locs = SimpleNamespace(**config['location'])
        print(locs.rewards.get(config['reward_count_dropdown']))

    def get_screen(self, title):
        return find_lushi_window(title)

    def test_screen_record(self):
        config = self.get_config()
        agent = lushi.Agent(config)
        agent.screen_record("test")
        self.assertEqual(True, True)

    def test_pick_treasure(self):
        config = self.get_config()
        agent = lushi.Agent(config)
        # image = self.get_save_image(2)
        # image = self.get_save_image(4)
        image = self.get_save_image(5)
        re = agent.pick_treasure(image)
        print(re)
        self.assertEqual(True, True)

    def test_choose_one_from_three(self):
        config = self.get_config()
        agent = lushi.Agent(config)
        image = self.get_save_image(6)
        re = agent.choose_one_from_three(image, "treasure")
        print(re)
        image = self.get_save_image(7)
        re = agent.choose_one_from_three(image, "heros")
        print(re)
        self.assertEqual(True, True)

    def test_pick_visitor(self):
        config = self.get_config()
        agent = lushi.Agent(config)
        image = self.get_save_image(3)
        re = agent.pick_visitor(image)
        print(re)
        self.assertEqual(True, True)

    def test_loc_click(self):
        config = self.get_config(lang='chs')
        self.locs = SimpleNamespace(**config['location'])
        rect, img = find_lushi_window('炉石传说')
        pyautogui.PAUSE = 0.5
        pyautogui.click(tuple_add(rect, self.locs.boss_page_right))
        pyautogui.click(tuple_add(rect, self.locs.boss_page_left))

    def test_hero_pos(self):
        a = [680, 810, 630, 240]  # 680, 810
        b = [465, 575]  # 偶数
        first_x = a[0]
        mid_x = a[1]
        n_my_hero = 6
        is_even = n_my_hero % 2 == 0
        for i in range(n_my_hero):
            x_offset = (mid_x - first_x) * (-n_my_hero // 2 + i + 1)
            if is_even:
                x_offset -= 65
            print(x_offset + mid_x)
        # 297                    550
        # 410 410                680
        # 523 523 523            810
        # 636 636                940
        # 749                    1070

        # 242                    485
        # 355 355                615
        # 468 468 468            745
        # 581 581 581            875
        # 694 694                1005
        # 807                    1135

    def test_submit_task(self):
        config = self.get_config(lang='eng')
        self.locs = SimpleNamespace(**config['location'])
        rect, img = find_lushi_window('hearthstone')
        pyautogui.PAUSE = 0.5
        for y in self.locs.tasks_y:
            for x in self.locs.tasks_x:
                # do task
                pyautogui.click(tuple_add(rect, (x, y)))
                pyautogui.click(tuple_add(rect, self.locs.tasks_abandon))
                pyautogui.click(tuple_add(rect, self.locs.tasks_abandon))
                pyautogui.click(tuple_add(rect, self.locs.tasks_abandon_cancel))
                pyautogui.click(tuple_add(rect, self.locs.tasks_abandon_cancel))
                pyautogui.click(tuple_add(rect, self.locs.campfire_exit))
                pyautogui.click(tuple_add(rect, self.locs.campfire_exit))
        # exit the campfire
        pyautogui.click(tuple_add(rect, self.locs.empty))
        # select first first boss of map
        pyautogui.click(tuple_add(rect, self.locs.first_boss))

    def test_scan_surprise_loc(self): 
        return None

    def test_any(self):
        a = [1, 2, 3]
        print(f'asdadasd sd {a}')


if __name__ == "__main__":
    unittest.main()
