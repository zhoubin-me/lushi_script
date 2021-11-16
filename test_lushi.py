# -*- coding: utf-8 -*-
from types import SimpleNamespace

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

    def get_save_image(self, to_gray = True):
        imgPath = os.path.join(".", "resource", "imgs_eng_1024x768", "img", "treasure2.png")
        src = cv2.imread(imgPath)
        if to_gray:
            image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        else:
            image = np.array(src)
        return image

    def get_config(self):
        config = {}
        
        try:
            with open('config/locs_eng.yaml', 'r', encoding='utf-8') as f:
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

    def test_pick_visitor(self):
        config = self.get_config()
        agent = lushi.Agent(config)
        _, image = self.get_screen("RustDesk")
        re = agent.pick_visitor(image, rect)
        print(re)
        self.assertEqual(True, True)

if __name__  == "__main__":
    unittest.main()