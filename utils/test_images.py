# -*- coding: utf-8 -*-
import unittest
from utils.util import find_lushi_window, find_icon_location
from utils.images import get_sub_np_array, get_burning_green_circles, get_burning_blue_lines
import yaml
from types import SimpleNamespace
import cv2
import numpy as np
import os

class TestImage(unittest.TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self) -> None:
        return super().tearDown()

    def gen_config(self):
        config = {}
        
        try:
            with open('config/default.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except:
            return ""

        config['screenshot_reward'] = True
        config['lang'] = 'EN-1024x768'

        loc_file = 'config/locs_eng.yaml'
        with open(loc_file, 'r', encoding='utf-8') as f:
            loc_cfg = yaml.safe_load(f)

        locs = SimpleNamespace(**loc_cfg['location'])
        return config, locs

    def get_screen(self, title):
        return find_lushi_window(title)

    def get_save_image(self, to_gray = True, imageName = "treasure2.png", lang="en"):
        a_path = "imgs_eng_1024x768"
        if "en" != lang :
            a_path = "imgs_chs_1600x900"

        imgPath = os.path.join(".", "resource", a_path, "img", imageName)
        src = cv2.imread(imgPath)
        if to_gray:
            image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        else:
            image = np.array(src)
        return image

    def read_sub_imgs(self, sub):
        self.img_folder = os.path.join(".", "resource", "imgs_eng_1024x768")
        self.treasure_blacklist = {}
        # treasure_blacklist
        imgs = [img for img in os.listdir(os.path.join(self.img_folder, sub)) if img.endswith('.png')]
        x = {}
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, sub, img)), cv2.COLOR_BGR2GRAY)
            x = getattr(self, sub)
            x[k] = v
        
        return x

    def test_get_sub_image(self):
        # _, screen = self.getScreen('RustDesk')
        screen = self.get_save_image()
        config, locs = self.gen_config()
        print(config, locs.treasures_locaion)
        
        imgMap = self.read_sub_imgs("treasure_blacklist")
        for key in self.treasure_blacklist.keys():
            for idx in range(1, 4):
                loc =  locs.treasures_locaion[idx]
                subImage = get_sub_np_array(screen, loc[0], loc[1], loc[2], loc[3])
                # success, X, Y, conf = match_sub_image(subImage, imgMap[key], 0.75)
                success, X, Y, conf = find_icon_location(subImage, imgMap[key], 0.75)
                print(f"test get_sub_image idx: {idx}, sub_key: {key}, suc: {success}, score: {conf}\n")

    def test_get_burning_green_circles(self):
        # screen = self.get_save_image( to_gray=False, imageName= "map_boss.png")
        # screen = self.get_save_image( to_gray=False, imageName= "cn_map2.png")
        screen = self.get_save_image( to_gray=False, imageName= "en_map3.png")
        # screen = self.get_save_image( to_gray=False, imageName= "map_blue.png")
        
        imgMap = get_burning_green_circles(screen, 55, 110)
        print(imgMap)

    def test_get_burning_blue_lines(self):
        screen = self.get_save_image( to_gray=False, imageName= "campfir1.png")
        # screen = self.get_save_image( to_gray=False, imageName= "map_blue.png")
        # screen = self.get_save_image( to_gray=False, imageName= "cn_campfire1.png", lang="cn")
        
        imgMap = get_burning_blue_lines(screen, 10, 300)
        print(imgMap)

if __name__  == "__main__":
    unittest.main()