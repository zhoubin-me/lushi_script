# -*- coding: utf-8 -*-
import random
import time
from types import SimpleNamespace

import pyautogui

import lushi
import main_gui
import unittest
import yaml
from utils.util import find_lushi_window, find_icon_location, restart_game, tuple_add, find_relative_loc


class TestLushi(unittest.TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self) -> None:
        return super().tearDown()

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
        config['lang'] = 'EN-1024x768'
        config['reward_count_dropdown'] = 3
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
        _, image = self.get_screen("RustDesk")
        re = agent.pick_treasure(image)
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

if __name__ == "__main__":
    unittest.main()
