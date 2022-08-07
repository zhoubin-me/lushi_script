# -*- coding: utf-8 -*-
import logging
import random
import traceback

import pyautogui
import cv2
import time
import numpy as np
import argparse
import os
import yaml
import datetime
from PIL import Image
from types import SimpleNamespace

from utils.log_util import LogUtil
from utils.util import BOSS_ID_MAP, find_lushi_window, find_icon_location, restart_game, tuple_add, find_relative_loc, \
    screenshot, find_lushi_raw_window, get_hero_color_by_id
from utils.images import get_sub_np_array, get_burning_green_circles, get_burning_blue_lines, get_burning_blue_lines, \
    get_dark_brown_lines
from utils.battle_ai import BattleAi
import utils.logging_util

logger = logging.getLogger()


class Agent:
    def __init__(self, cfg):
        if cfg['lang'].startswith('EN'):
            self.lang = 'eng'
            self.loc_file = 'config/locs_eng.yaml'
            self.img_folder = 'resource/imgs_eng_1024x768'
            self.title = 'hearthstone'
        elif cfg['lang'].startswith('ZH'):
            self.lang = 'chs'
            self.loc_file = 'config/locs_chs.yaml'
            self.img_folder = "resource/imgs_chs_1600x900"
            self.title = "炉石传说"
        else:
            raise ValueError(f"Language {cfg['lang']} is not supported yet")

        self.debug = False  # TODO check before commit, 什么时候把这个也做到按钮里
        self.icons = {}
        self.treasure_whitelist = {}
        self.treasure_blacklist = {}
        self.heros_whitelist = {}
        self.heros_blacklist = {}
        self.game = None
        self.skill_seq_cache = {}
        self.boss_skill_seq_cache = {}
        self.start_seq = {}
        self.side = None
        self.surprise_in_mid = False
        self.surprise_relative_loc = None
        self.lettuce_role_limit = 2
        self.battle_stratege = "normal"
        self.boss_battle_stratege = "normal"
        self.stop_at_boss = False
        self.choice_skill_index = 0  # 抉择技能选择第1个
        self.battle_time_wait = 1
        self.states = ['box', 'mercenaries', 'team_lock', 'travel', 'boss_list', 'team_list', 'map_not_ready',
                       'goto', 'show', 'teleport', 'start_game', 'member_not_ready', 'not_ready_dots', 'battle_ready',
                       'treasure_list', 'treasure_replace', 'treasure_list2', 'destroy', 'blue_portal', 'boom', 'visitor_list',
                       'final_reward', 'final_reward2', 'final_confirm', 'close', 'ok', 'done', 'member_not_ready2','boss_empty_icon', 'campfire']

        self.load_config(cfg)
        self.log_util = LogUtil(self.basic.hs_log)

    def new_click(self, arg0=None, arg1=None):
        if arg0 == None:
            pyautogui.click()
        elif arg1 == None:
            pyautogui.click(arg0[0] + self.fix_x, arg0[1] + self.fix_y)
        else:
            pyautogui.click(arg0 + self.fix_x, arg1 + self.fix_y)

    def read_sub_imgs(self, sub):
        imgs = [img for img in os.listdir(os.path.join(self.img_folder, sub)) if img.endswith('.png')]
        for img in imgs:
            k = img.split('.')[0]
            v = cv2.cvtColor(cv2.imread(os.path.join(self.img_folder, sub, img)), cv2.COLOR_BGR2GRAY)
            x = getattr(self, sub)
            x[k] = v

    def load_config(self, cfg):
        with open(self.loc_file, 'r', encoding='utf-8') as f:
            loc_cfg = yaml.safe_load(f)

        self.locs = SimpleNamespace(**loc_cfg['location'])
        for sub in ['icons', 'treasure_blacklist', 'treasure_whitelist', 'heros_whitelist', 'heros_blacklist']:
            self.read_sub_imgs(sub)

        hero_info = cfg['hero']
        self.heros = {}
        for k, v in hero_info.items():
            spell_order = [int(x) - 1 for x in v[2].split(',')]
            self.heros[k] = [v[0], v[1], spell_order, v[3], get_hero_color_by_id(k)]
            self.skill_seq_cache[k] = v[-2]
        del cfg['hero']
        # boss encounter hero
        self.boss_heros = {}
        if 'boss_hero' in cfg:
            boss_hero_info = cfg['boss_hero']
            for k, v in boss_hero_info.items():
                spell_order = [int(x) - 1 for x in v[2].split(',')]
                self.boss_heros[k] = [v[0], v[1], spell_order, v[3], get_hero_color_by_id(k)]
                self.boss_skill_seq_cache[k] = v[-2]
            del cfg['boss_hero']
        else:
            self.boss_heros = self.heros
        cfg['hs_log'] = os.path.join(os.path.dirname(cfg['hs_path']), 'Logs', 'Power.log')
        self.basic = SimpleNamespace(**cfg)
        self.stop_at_boss = self.basic.stop_at_boss
        self.fix_x = self.basic.fix_x
        self.fix_y = self.basic.fix_y
        self.lettuce_role_limit = int(self.basic.lettuce_role_limit)
        self.map_decision = self.basic.map_decision
        if self.map_decision is None or self.map_decision == '':
            self.map_decision = 'visitor_first'
        self.battle_time_wait = self.basic.battle_time_wait  # 战斗休眠时间
        if self.battle_time_wait is None or self.battle_time_wait == '':
            self.battle_time_wait = 1
        self.choice_skill_index = self.basic.choice_skill_index  # 技能抉择
        if self.choice_skill_index is None or self.choice_skill_index == '':
            self.choice_skill_index = 0
        pyautogui.PAUSE = self.basic.delay

    def check_in_screen(self, name, prefix='icons'):

        rect, screen = find_lushi_window(self.title)
        try:
            icon = getattr(self, prefix)[name]
        except:
            return False, None, None
        success, X, Y, conf = find_icon_location(screen, icon, self.basic.confidence)
        del screen
        loc = X, Y
        return success, loc, rect

    # 检查并获取图片
    def check_and_screen(self, name, prefix='icons'):
        rect, screen = find_lushi_window(self.title)
        try:
            icon = getattr(self, prefix)[name]
        except:
            return False, None, None, None
        success, X, Y, conf = find_icon_location(screen, icon, self.basic.confidence)
        loc = X, Y
        return success, loc, rect, screen

    # 传入图片，匹配子图
    def find_in_image(self, screen, name, prefix='icons'):
        try:
            icon = getattr(self, prefix)[name]
        except:
            return False, None, None
        success, X, Y, conf = find_icon_location(screen, icon, self.basic.confidence)
        del screen
        loc = X, Y
        return success, loc, conf

    def scan_surprise_loc(self, rect, img_name='surprise'):
        # time.sleep(5)
        logger.info(f'Scanning surprise, rect: {rect}')
        pyautogui.moveTo(tuple_add(rect, self.locs.scroll))
        tic = time.time()
        while True:
            success, loc, rect = self.check_in_screen(img_name)
            if success:
                logger.info(f"Found surprise at start {loc}")
                return loc
            if self.check_in_screen('start_point')[0]:
                break
            if time.time() - tic > 10:
                return

        screen_images = []
        for i in range(10):
            success, loc, rect, the_img = self.check_and_screen(img_name)
            if 0 == i % 2 or success:
                _, the_img = find_lushi_window(self.title, to_gray=False, raw=True)
                # the_img.save("first_img.png")
                the_map_loc = self.locs.map_location
                sub_img = get_sub_np_array(the_img, the_map_loc[0], the_map_loc[1], the_map_loc[2],
                                           the_map_loc[3])  # [230, 80, 810, 620]
                screen_images.append(sub_img)
            if success:
                for _ in range(10):
                    pyautogui.scroll(-60)
                logger.info(f"Found surprise during scrolling {loc}")
                # full_map = images_to_full_map(screen_images)
                # cv2.imwrite("full_map_res3.jpg", full_map) # TODO rmove before submit
                return loc

            pyautogui.scroll(60)  # 先截图，再滑

        logger.info("Did not found any surprise")
        return None

    def scan_surprise_in_map_loc(self, rect, img_name='surprise'):
        # time.sleep(5)
        logger.info(f'Scanning surprise, rect: {rect}')
        pyautogui.moveTo(tuple_add(rect, self.locs.scroll))
        tic = time.time()
        while True:
            success, loc, rect = self.check_in_screen("surprise")
            if success:
                logger.info(f"Found surprise at {loc}")
                return loc
            success, loc, rect = self.check_in_screen("off_surprise")
            if success:
                logger.info(f"Found off surprise at {loc}")
                return loc
            if self.check_in_screen('start_point')[0]:
                break
            if self.check_in_screen('map_not_ready')[0]:
                break
            if time.time() - tic > 10:
                return

        screen_images = []
        for i in range(10):
            success, loc, rect, the_img = self.check_and_screen("surprise")
            if not success:
                success, loc, rect = self.check_in_screen("off_surprise")
            if success:
                logger.info(f"Found off/on surprise at  {loc}")
                return loc
            if 0 == i % 2:
                _, the_img = find_lushi_window(self.title, to_gray=False, raw=True)
                # the_img.save("first_img.png")
                the_map_loc = self.locs.map_location
                sub_img = get_sub_np_array(the_img, the_map_loc[0], the_map_loc[1], the_map_loc[2],
                                           the_map_loc[3])  # [230, 80, 810, 620]
                screen_images.append(sub_img)
            if success:
                for _ in range(10):
                    pyautogui.scroll(-60)
                # full_map = images_to_full_map(screen_images)
                # cv2.imwrite("full_map_res2.jpg", full_map) # TODO remove befre commit 
                return loc

            pyautogui.scroll(60)  # 先截图，再滑

        logger.info("Did not found any surprise")
        return None

    def task_submit(self, rect):

        if self.basic.auto_tasks:
            logger.info('Start submit task...')
            # select Camp Fire
            self.new_click(tuple_add(rect, self.locs.campfire))
            # pyautogui.click(tuple_add(rect, self.locs.start_game)) # 新版本不需要点这一下了
            # check if a task finish
            time.sleep(1)
            _, img = find_lushi_window(self.title, to_gray=False, raw=True)
            lines = get_burning_blue_lines(img)
            if None is not lines and 0 < len(lines):
                logger.info("some task finished ... ")
                for y in self.locs.tasks_y:
                    for x in self.locs.tasks_x:
                        # do task
                        self.new_click(tuple_add(rect, (x, y)))
                        self.new_click(tuple_add(rect, self.locs.tasks_abandon))
                        self.new_click(tuple_add(rect, self.locs.tasks_abandon_cancel))
                        self.new_click(tuple_add(rect, self.locs.tasks_abandon_cancel))
                        self.new_click(tuple_add(rect, self.locs.campfire_exit))

            # exit the campfire
            self.new_click(tuple_add(rect, self.locs.empty))
            # select first first boss of map
            self.new_click(tuple_add(rect, self.locs.first_boss))

    def start_battle(self, rect, battle_boss=False):
        logger.info(f"Start battle, boss ? {battle_boss}, scanning battlefield")
        # rect, screen = find_lushi_window(self.title)
        # check if battle boss
        battle_stratege = self.basic.battle_stratege  # normal, max_dmg, kill_big, kill_min
        if battle_boss:
            battle_stratege = self.basic.boss_battle_stratege  # normal, max_dmg, kill_big, kill_min

        del self.log_util
        self.log_util = LogUtil(self.basic.hs_log)
        game = self.log_util.parse_game()

        first_x, mid_x, last_x, y = self.locs.heros
        n_my_hero = len(game.my_hero)
        is_even = n_my_hero % 2 == 0
        for i in range(n_my_hero):
            x_offset = (mid_x - first_x) * (-n_my_hero // 2 + i + 1)
            if is_even:
                x_offset -= (mid_x - first_x) // 2
            game.my_hero[i].set_pos(mid_x + x_offset + rect[0], y + rect[1])

        first_x, mid_x, last_x, y = self.locs.enemies
        n_enemy_hero = len(game.enemy_hero)
        is_even = n_enemy_hero % 2 == 0
        for i in range(n_enemy_hero):
            x_offset = (mid_x - first_x) * (-n_enemy_hero // 2 + i + 1)
            if is_even:
                x_offset -= (mid_x - first_x) // 2
            game.enemy_hero[i].set_pos(mid_x + x_offset + rect[0], y + rect[1])

        strategy = BattleAi.battle(game.my_hero, game.enemy_hero, battle_stratege) # [0,1,1]
        if 1 > len(strategy):
            # 检查策略是否为空，为空说明不可选择，直接跳过
            self.new_click(tuple_add(rect, self.locs.start_battle))

        self.new_click(tuple_add(rect, self.locs.empty))

        standby_heros = self.heros
        if battle_boss:
            standby_heros = self.boss_heros
        for hero_i, h in enumerate(game.my_hero):
            if h.lettuce_has_manually_selected_ability:
                continue

            self.new_click(h.pos)
            card_id = h.card_id[:-3]
            att_skill_id = 0
            if card_id not in standby_heros:
                other_skill_id = 0  # 非预期角色的技能干预
                if True == battle_boss:
                    if card_id == "LETL_848H6" or card_id == "LETL_84":  # npc 瓦莉拉
                        if len(h.spell) > 2 and 1 > h.spell[2].lettuce_current_cooldown:
                            att_skill_id = other_skill_id = 2
                if card_id.startswith("LETL_024P2_"):  # 尤多拉 炮台
                    if len(h.spell) > 2 and 1 > h.spell[2].lettuce_current_cooldown:
                        att_skill_id = other_skill_id = 2
                if card_id.startswith("LT22_002E3_"):  # 巴琳达的火元素
                    if len(h.spell) > 1 and 1 > h.spell[1].lettuce_current_cooldown:
                        att_skill_id = other_skill_id = 1
                if card_id.startswith("LETL_823H3"): # 小鬼魔仆
                    if len(h.spell) > 1 and 1 > h.spell[1].lettuce_current_cooldown:
                        att_skill_id = other_skill_id = 1
                if card_id.startswith("LETL_861H3"): # 0/500 石槌战旗
                    if len(h.spell) > 1 and 1 > h.spell[1].lettuce_current_cooldown:
                        att_skill_id = other_skill_id = 1
                if card_id.startswith("LETL_866H2"): # 0/150 净化碎片
                    if len(h.spell) > 2 and 1 > h.spell[2].lettuce_current_cooldown:
                        att_skill_id = other_skill_id = 2
                skill_loc = tuple_add(rect, (self.locs.skills[other_skill_id], self.locs.skills[-1]))
            else:
                skill_loc = None
                skill_seq = standby_heros[card_id][2]
                # 需要考虑低等级佣兵，不够3个技能
                for skill_id in skill_seq:
                    print(f"type {type(h.spell)}")
                    if skill_id < len(h.spell):

                        skill_cooldown_round = h.spell[skill_id].lettuce_current_cooldown
                        if skill_cooldown_round == 0:
                            skill_loc = tuple_add(rect, (self.locs.skills[skill_id], self.locs.skills[-1]))
                            att_skill_id = skill_id
                            break
                    else:
                        continue
            self.new_click(skill_loc)
            self.new_click(tuple_add(rect, (self.locs.choice_skills[self.choice_skill_index], self.locs.choice_skills[-1])))
            enemy_id = strategy[hero_i]
            print(
                f"debug hero_id {hero_i} card_id {card_id} attack enemy {enemy_id} by skill {att_skill_id} use strategy {strategy}")
            self.new_click(game.enemy_hero[enemy_id].pos)
            self.new_click(tuple_add(rect, self.locs.empty))

    # risk_num  颜色克制的敌人回避数量阈值，大于该数值则需要调整上场英雄
    def select_members(self, risk_num=2, battle_boss=False):
        logger.info(f"Start select members, battle_boss ? {battle_boss} start battle enemy")
        game = self.log_util.parse_game()
        rect, screen = find_lushi_window(self.title, to_gray=False)
        del screen
        enemy_blue_count = 0
        enemy_green_count = 0
        enemy_red_count = 0
        for hero in game.enemy_hero:
            logger.info(
                f"enemy is car_id {hero.card_id}, hp {hero.max_health}, atk {hero.atk}, color {hero.lettuce_role}, entity_id {hero.entity_id}")
            if hero.get_lettuce_role() == 1:
                enemy_blue_count += 1
            elif hero.get_lettuce_role() == 2:
                enemy_green_count += 1
            elif hero.get_lettuce_role() == 3:
                enemy_red_count += 1
        normal = True
        if risk_num > 0 and (risk_num < enemy_blue_count or risk_num < enemy_green_count or risk_num < enemy_red_count):
            normal = False

        hero_on_battlefie_limit = 4  # if battle boss
        standby_heros = self.heros
        if battle_boss:
            standby_heros = self.boss_heros
        hero_in_battle = [h for h in game.my_hero if h.card_id[:-3] in standby_heros]
        if len(hero_in_battle) < hero_on_battlefie_limit:
            current_seq = {h.card_id[:-3]: i for i, h in enumerate(game.setaside_hero)}
            heros_sorted = {k: v[3] for k, v in sorted(
                standby_heros.items(), key=lambda item: item[1][3])}
            card_id_seq = list(heros_sorted.keys())
            card_id_seq = [x for x in card_id_seq if x in current_seq]

            for i in range(3 - len(hero_in_battle)):
                if len(card_id_seq) > 0:

                    cards_in_hand = len(card_id_seq)
                    card_id = -1
                    i = 0
                    if battle_boss or normal:
                        card_id = card_id_seq.pop(0)
                    elif enemy_blue_count > risk_num:
                        for k in card_id_seq:
                            if int(standby_heros[k][4]) != 3:
                            # if int(standby_heros[k][4]) == 2:
                                card_id = k
                                del card_id_seq[i]
                                break
                            i += 1
                    elif enemy_green_count > risk_num:
                        for k in card_id_seq:
                            if int(standby_heros[k][4]) != 1:
                            # if int(standby_heros[k][4]) == 3:
                                card_id = k
                                del card_id_seq[i]
                                break
                            i += 1
                    elif enemy_red_count > risk_num:
                        for k in card_id_seq:
                            if int(standby_heros[k][4]) != 2:
                            # if int(standby_heros[k][4]) == 1:
                                card_id = k
                                del card_id_seq[i]
                                break
                            i += 1

                    if card_id == -1:  # 兜底
                        card_id = card_id_seq.pop(0)

                    first_x, last_x, y = self.locs.members
                    mid_x = (first_x + last_x) // 2
                    current_pos = current_seq[card_id]

                    if cards_in_hand > 3:
                        dis = (last_x - first_x) // (cards_in_hand - 1)
                        loc = (first_x + dis * current_pos, y)
                    elif cards_in_hand == 3:
                        loc = (mid_x + self.locs.members_distance * (current_pos - 1), y)
                    elif cards_in_hand == 2:
                        if current_pos == 0:
                            factor = -1
                        elif current_pos == 1:
                            factor = 1
                        else:
                            raise ValueError("Not possible")

                        loc = (mid_x + self.locs.members_distance // 2 * factor, y)
                    elif cards_in_hand == 1:
                        loc = (mid_x, y)
                    else:
                        raise ValueError("Not possible")  # no heros fight for you

                    self.new_click(tuple_add(rect, loc))
                    pyautogui.moveTo(tuple_add(rect, self.locs.dragto))
                    self.new_click()

                    del current_seq[card_id]
                    for k, v in current_seq.items():
                        if v > current_pos:
                            current_seq[k] = v - 1
                else:
                    # 如果佣兵和策略不匹配，直接点确认。
                    self.new_click(tuple_add(rect, self.locs.start_battle))

    # 神秘人、技能宝藏，三选一通用方法, pick_type:  treasure/heros
    def choose_one_from_three(self, screen, pick_type = "treasure"):
        is_in_whitelist = False
        is_in_blacklist = False
        idx_white_list = []
        idx_black_list = []

        locations = []
        img_prefix = pick_type
        white_img_names = []
        black_img_names = []
        if "heros" == pick_type :
            locations = self.locs.visitors_location.items()
            white_img_names = self.heros_whitelist.keys()
            black_img_names = self.heros_blacklist.keys()
        else:
            locations = self.locs.treasures_location.items()
            white_img_names = self.treasure_whitelist.keys()
            black_img_names = self.treasure_blacklist.keys()

        for key in white_img_names:
            success, loc, conf = self.find_in_image(screen, key, prefix= img_prefix + '_whitelist')
            if success and 0.9 < conf: # TODO config 这里要单独拎出来
                is_in_whitelist = True
                dist = 1024
                the_index = 0
                for idx, v_loc in locations:
                    new_dist = abs(loc[0] - v_loc[2])
                    if new_dist < dist:  # right_x - right_x
                        the_index = idx
                        dist = new_dist

                idx_white_list.append(the_index)

        # 去重
        idx_white_list = list(set(idx_white_list))
        if is_in_whitelist and 0 < len(idx_white_list):
            logger.info(f'find visitor white list {idx_white_list}')
            return idx_white_list

        for key in black_img_names:
            success, loc, conf = self.find_in_image(screen, key, prefix= img_prefix + '_blacklist')
            if success and 0.85 < conf : # TODO config
                is_in_blacklist = True
                dist = 1024
                the_index = 0
                for idx, v_loc in locations:
                    new_dist = abs(loc[0] - v_loc[2])
                    if new_dist < dist:  # right_x - right_x
                        the_index = idx
                        dist = new_dist

                idx_black_list.append(the_index)

        # 去重
        idx_black_list = list(set(idx_black_list))

        if is_in_blacklist:
            logger.info(f'find visitor black list {idx_black_list}')
            if 2 < len(idx_black_list) or 1 > len(idx_black_list):
                return [0, 1, 2]
            else:
                advice_idx = []
                for idx in range(3):
                    if idx not in idx_black_list:
                        advice_idx.append(idx)
                return advice_idx

        return [0, 1, 2]  # 兜底返回

    # 从按照黑名单剔除宝藏，返回可选项，如果没有则返回[0], 最多返回：[0,1,2]
    def pick_treasure(self, screen):
        advice_idx = []
        not_advice_idx = []
        for key in self.treasure_blacklist.keys():
            for idx in range(3):
                loc = self.locs.treasures_location[idx]
                one_treasure = get_sub_np_array(screen, loc[0], loc[1], loc[2], loc[3])
                success, X, Y, conf = find_icon_location(one_treasure, self.treasure_blacklist[key],
                                                         self.basic.confidence)
                if success and idx not in not_advice_idx:
                    not_advice_idx.append(idx)
                    if 1 < len(not_advice_idx):
                        break
            if 1 < len(not_advice_idx):
                break

        logger.info(f'find treasure blacklist: {not_advice_idx}')
        if 2 < len(not_advice_idx) or 1 > len(not_advice_idx):
            return [0, 1, 2]
        else:
            for idx in range(3):
                if idx not in not_advice_idx:
                    advice_idx.append(idx)
            return advice_idx

    # 按照黑白名单选择神秘人选项，白名单命中，则选白名单的。黑名单命中则不选，如果白名单没命中，黑名单全命中，则随机选
    def pick_visitor(self, screen):
        is_in_whitelist = False
        is_in_blacklist = False
        idx_white_list = []
        idx_black_list = []
        for key in self.heros_whitelist.keys():
            success, loc, conf = self.find_in_image(screen, key, prefix='heros_whitelist')
            if success:
                is_in_whitelist = True
                dist = 1024
                the_index = 0
                for idx, v_loc in self.locs.visitors_location.items():
                    new_dist = abs(loc[0] - v_loc[2])
                    if new_dist < dist:  # right_x - right_x
                        the_index = idx
                        dist = new_dist

                idx_white_list.append(the_index)

        # 去重
        idx_white_list = list(set(idx_white_list))
        if is_in_whitelist and 0 < len(idx_white_list):
            logger.info(f'find visitor white list {idx_white_list}')
            return idx_white_list

        for key in self.heros_blacklist.keys():
            success, loc, conf = self.find_in_image(screen, key, prefix='heros_blacklist')
            if success:
                is_in_blacklist = True
                dist = 1024
                the_index = 0
                for idx, v_loc in self.locs.visitors_location.items():
                    new_dist = abs(loc[0] - v_loc[2])
                    if new_dist < dist:  # right_x - right_x
                        the_index = idx
                        dist = new_dist

                idx_black_list.append(the_index)

        # 去重
        idx_black_list = list(set(idx_black_list))

        if is_in_blacklist:
            logger.info(f'find visitor black list {idx_black_list}')
            if 2 < len(idx_black_list) or 1 > len(idx_black_list):
                return [0, 1, 2]
            else:
                advice_idx = []
                for idx in range(3):
                    if idx not in idx_black_list:
                        advice_idx.append(idx)
                return advice_idx

        return [0, 1, 2]  # 兜底返回
    
    def submit_campfire_mission(self, rect):
        logger.info("campfire dialog")
        time.sleep(1)
        _, img = find_lushi_window(self.title, to_gray=False, raw=True)
        lines = get_burning_blue_lines(img)
        if None is not lines and 0 < len(lines):
            logger.info("some task finished ... ")
            for y in self.locs.tasks_y:
                for x in self.locs.tasks_x:
                    # do task
                    self.new_click(tuple_add(rect, (x, y)))
                    self.new_click(tuple_add(rect, self.locs.tasks_abandon))
                    self.new_click(tuple_add(rect, self.locs.tasks_abandon_cancel))
                    self.new_click(tuple_add(rect, self.locs.tasks_abandon_cancel))
                    self.new_click(tuple_add(rect, self.locs.campfire_exit))

        # exit the campfire
        self.new_click(tuple_add(rect, self.locs.empty))

    def state_handler(self, state, tic, text):
        success, loc, rect = self.check_in_screen(text)
        '''
        self.states = ['box', 'mercenaries', 'team_lock', 'travel', 'boss_list','team_list', 'map_not_ready',
                  'goto', 'show', 'teleport', 'start_game', 'member_not_ready', 'not_ready_dots', 'battle_ready',
                  'treasure_list', 'treasure_replace', 'treasure_list2', 'destroy', 'blue_portal', 'boom', 'visitor_list',
                  'final_reward', 'final_reward2', 'final_confirm', 'ok', 'close', 'done', 'member_not_ready2', 'boss_empty_icon', 'campfire']
        '''
        if success:
            if state != text:
                state = text
                tic = time.time()

            if state in ['mercenaries', 'box', 'team_lock', 'close', 'ok', 'done']:
                logger.info(f'find {state}, try to click')
                self.new_click(tuple_add(rect, loc))

            if state == 'travel':
                logger.info(f'find {state}, try to click')
                self.surprise_relative_loc = None  # 进地图清空
                self.new_click(tuple_add(rect, loc))
                time.sleep(1) # 避免误触信箱
                self.new_click(tuple_add(rect, self.locs.travel))

            if state == 'boss_list' or 'boss_empty_icon' == state :
                logger.info('find boss list, try to click')
                the_boss_id = 0
                if self.basic.boss_id in BOSS_ID_MAP:
                    the_boss_id = BOSS_ID_MAP[self.basic.boss_id]
                if the_boss_id > 19:
                    # boss 8-7,8,9,10
                    self.new_click(tuple_add(rect, self.locs.boss_page_right))
                    time.sleep(1)
                    the_loc = getattr(self.locs, "boss_{}_of_4".format(the_boss_id - 19))
                    self.new_click(tuple_add(rect, the_loc))
                    self.new_click(tuple_add(rect, self.locs.start_game))
                elif the_boss_id > 15:
                    # boss 7-1,2,3,4
                    the_loc = getattr(self.locs, "boss_{}_of_4".format(the_boss_id - 15))
                    self.new_click(tuple_add(rect, the_loc))
                    self.new_click(tuple_add(rect, self.locs.start_game))
                elif the_boss_id > 14:
                    # boss 13
                    self.new_click(tuple_add(rect, self.locs.boss_page_right))
                    time.sleep(1)
                    self.new_click(tuple_add(rect, self.locs.boss_page_right))
                    self.new_click(tuple_add(rect, self.locs.boss_4_13))
                    self.new_click(tuple_add(rect, self.locs.start_game))
                elif the_boss_id > 8:
                    the_id = the_boss_id - 9
                    x_id = the_id % 3
                    y_id = the_id // 3
                    loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])
                    self.new_click(tuple_add(rect, self.locs.boss_page_left))
                    time.sleep(0.5)
                    self.new_click(tuple_add(rect, self.locs.boss_page_left))
                    time.sleep(0.5)
                    self.new_click(tuple_add(rect, self.locs.boss_page_right))
                    self.new_click(tuple_add(rect, loc))
                    self.new_click(tuple_add(rect, self.locs.start_game))
                elif the_boss_id > 5:
                    id_standard = (the_boss_id - 6) * 2
                    x_id = id_standard % 3
                    y_id = id_standard // 3
                    loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])

                    self.new_click(tuple_add(rect, self.locs.boss_page_left))
                    time.sleep(0.5)
                    self.new_click(tuple_add(rect, self.locs.boss_page_left))
                    time.sleep(0.5)
                    self.new_click(tuple_add(rect, self.locs.boss_page_right))
                    self.new_click(tuple_add(rect, loc))
                    self.new_click(tuple_add(rect, self.locs.start_game))
                else:
                    x_id = the_boss_id % 3
                    y_id = the_boss_id // 3
                    loc = (self.locs.boss[x_id], self.locs.boss[3 + y_id])
                    self.new_click(tuple_add(rect, self.locs.boss_page_left))
                    time.sleep(0.5)
                    self.new_click(tuple_add(rect, self.locs.boss_page_left))
                    time.sleep(0.5)
                    self.new_click(tuple_add(rect, loc))
                    self.new_click(tuple_add(rect, self.locs.start_game))

            if state == 'team_list':
                logger.info(f'find {state}, try to click')
                x_id = self.basic.team_id % 3
                y_id = self.basic.team_id // 3

                self.new_click(tuple_add(rect, (self.locs.teams[x_id], self.locs.teams[3 + y_id])))
                self.new_click(tuple_add(rect, self.locs.team_select))
                self.new_click(tuple_add(rect, self.locs.team_lock))
                time.sleep(7)  # avoid too low speed of entering map action to skip task_submit and scan_surprise
                self.task_submit(rect)
                # if self.basic.boss_id != 0:
                time.sleep(1)
                # 通关策略
                surprise_loc = None
                if self.map_decision == "visitor_first":
                    surprise_loc = self.scan_surprise_loc(rect)
                    self.surprise_relative_loc = surprise_loc
                else:
                    self.surprise_relative_loc = None

                if surprise_loc is not None:
                    if surprise_loc[0] < self.locs.start_point[0]:
                        self.side = 'left'
                    else:
                        self.side = 'right'
                    first_x, mid_x, last_x, y = self.locs.focus
                    if np.abs(surprise_loc[0] - mid_x) < 100:
                        self.surprise_in_mid = True
                    else:
                        self.surprise_in_mid = False
                    logger.info(f'Surprise side {self.side}, surprise in middile {self.surprise_in_mid}')

            if state == 'campfire':
                logger.info(f'find {state}, try to click') 
                self.submit_campfire_mission(rect)
            
            if state == 'map_not_ready':
                logger.info(f'find {state}, try to click next map')
                _, screen = find_lushi_raw_window(self.title)
                the_map_loc = self.locs.map_location  # 只选取部分
                screen = get_sub_np_array(screen, the_map_loc[0], the_map_loc[1], the_map_loc[2],
                                          the_map_loc[3])  # [230, 80, 810, 620]
                circles = get_burning_green_circles(screen, 55, 110)
                if self.surprise_relative_loc is None and "visitor_first" == self.map_decision:  # 找下 漩涡的相对坐标
                    # success, loc, rect, the_img = self.check_and_screen('surprise')
                    surprise_loc = self.scan_surprise_in_map_loc(rect, img_name='off_surprise')
                    self.surprise_relative_loc = surprise_loc
                    # 翻了地图要回来
                    for i in range(-10, 10):
                        _, screen = find_lushi_raw_window(self.title)
                        screen = get_sub_np_array(screen, the_map_loc[0], the_map_loc[1], the_map_loc[2],
                                                  the_map_loc[3])  # [230, 80, 810, 620]
                        circles = get_burning_green_circles(screen, 55, 110)
                        if circles is not None and len(circles) > 0:
                            break

                        if i < 0:
                            pyautogui.scroll(-60)
                        else:
                            pyautogui.scroll(60)

                if circles is not None and 0 < len(circles):
                    if self.map_decision == "visitor_first":
                        loc = self.surprise_relative_loc
                        min_loc = None
                        if None != loc and 0 < len(loc):
                            dist = 1024
                            for v_loc in circles[0, :]:  # 遍历矩阵每一行的数据
                                new_dist = abs(loc[0] - (v_loc[0] + the_map_loc[0]))
                                if new_dist < dist:  # right_x - right_x
                                    min_loc = v_loc
                                    dist = new_dist
                        else:
                            locs = circles[0, :]
                            min_loc = locs[-1]

                        min_loc[1] = min_loc[1] + the_map_loc[1]  # sub image y ++
                        min_loc[0] = min_loc[0] + the_map_loc[0]
                        logger.info(f'chose the  {min_loc}, to start game')
                        self.new_click(tuple_add(rect, (min_loc[0], min_loc[1])))
                        # check start_game:
                        success, loc, _ = self.check_in_screen("map_not_ready")
                        if success:
                            self.new_click(tuple_add(rect, self.locs.map_back))

                    else:
                        i = 0
                        battle_idx = []
                        for v_loc in circles[0, :]:  # 遍历矩阵每一行的数据
                            cur_loc = [0, 0]
                            cur_loc[1] = v_loc[1] + the_map_loc[1]  # sub image y ++
                            cur_loc[0] = v_loc[0] + the_map_loc[0]
                            self.new_click(tuple_add(rect, cur_loc))
                            success, _, _ = self.check_in_screen("start_game")
                            if success:
                                battle_idx.append(i)
                            i += 1
                        i = 0
                        for v_loc in circles[0, :]:  # 遍历矩阵每一行的数据
                            if i not in battle_idx or 1 < len(battle_idx):
                                cur_loc = [0, 0]
                                cur_loc[1] = v_loc[1] + the_map_loc[1]  # sub image y ++
                                cur_loc[0] = v_loc[0] + the_map_loc[0]
                                self.new_click(tuple_add(rect, cur_loc))
                                break
                            i += 1

                else:  # 兜底action
                    first_x, mid_x, last_x, y = self.locs.focus
                    if self.side is None:
                        self.side = 'left'
                    if self.side == 'left':
                        if self.surprise_in_mid:
                            x1, x2, x3 = first_x, (first_x + mid_x) // 2, mid_x
                        else:
                            x1, x2, x3 = mid_x, (first_x + mid_x) // 2, first_x
                    else:
                        if self.surprise_in_mid:
                            x1, x2, x3 = last_x, (last_x + mid_x) // 2, mid_x
                        else:
                            x1, x2, x3 = mid_x, (last_x + mid_x) // 2, last_x

                    for x in (x1, x2, x3):
                        self.new_click(tuple_add(rect, (x, y)))

            if state in ['goto', 'show', 'teleport', 'start_game']:
                logger.info(f'find {state}, try to click')
                if self.stop_at_boss:
                    # 检查是否进入boss关卡
                    success, loc, rect = self.check_in_screen("final_boss")
                    if success:
                        _, screen = find_lushi_raw_window(self.title)
                        the_map_loc = self.locs.no_boss_map_location  # 只选取部分
                        screen = get_sub_np_array(screen, the_map_loc[0], the_map_loc[1], the_map_loc[2],
                                                  the_map_loc[3])
                        circles = get_burning_green_circles(screen, 55, 110)
                        if 1 > len(circles):
                            print(f"[{state}]  stop at boss")
                            time.sleep(30)
                else:
                    self.new_click(tuple_add(rect, self.locs.start_game))

            if state in ['member_not_ready', 'member_not_ready2']:
                logger.info(f'find {state}, try to click')
                _, screen = find_lushi_window(self.title, to_gray=False, raw=True)
                loc = self.locs.boss_battlefield
                subImage = get_sub_np_array(screen, loc[0], loc[1], loc[2], loc[3])
                lines = get_dark_brown_lines(subImage)
                battle_boss = False
                if 2 < len(lines):
                    battle_boss = True
                    logger.info(f'[{state}] battle boss')
                    # screenshot(self.title, state) # TODO commit before 
                self.select_members(self.lettuce_role_limit, battle_boss)

            if state == 'not_ready_dots':
                logger.info(f'find {state}, try to click')
                # check if battle boss
                _, screen = find_lushi_window(self.title, to_gray=False, raw=True)
                loc = self.locs.boss_battlefield
                subImage = get_sub_np_array(screen, loc[0], loc[1], loc[2], loc[3])
                lines = get_dark_brown_lines(subImage)
                battle_boss = False
                if 2 < len(lines):
                    battle_boss = True
                    logger.info(f'[{state}] battle boss')

                logger.info(f'find {state}, try to click，and sleep {self.battle_time_wait} second')
                time.sleep(self.battle_time_wait)

                self.start_battle(rect, battle_boss)

            if state == 'battle_ready':
                # logger.info(f'find {state}, try to click，and sleep {self.battle_time_wait} second')
                # time.sleep(self.battle_time_wait)
                self.new_click(tuple_add(rect, self.locs.start_battle))

            if state in ['treasure_list', 'treasure_replace', 'treasure_list2']:
                logger.info(f'find {state}, try to click')
                if self.debug or self.basic.screenshot_treasure:
                    screenshot(self.title, 'treasure[xx]')
                _, screen = find_lushi_window(self.title)
                # advice = self.pick_treasure(screen)
                advice = self.choose_one_from_three(screen, "treasure")

                t_id = random.choice(advice)
                treasure_loc = (self.locs.treasures[t_id], self.locs.treasures[-1])
                logger.info(f"click treasure : {t_id} at locs {treasure_loc}")

                self.new_click(tuple_add(rect, treasure_loc))
                # hero treasure screenshot before confirm
                if self.debug or self.basic.screenshot_treasure:
                    screenshot(self.title, f'treasure[{",".join(str(i) for i in advice)}]')
                self.new_click(tuple_add(rect, self.locs.treasures_collect))
                del screen

            if state in ['destroy', 'blue_portal', 'boom']:
                logger.info(f'find {state}, try to click')
                if self.basic.early_stop:
                    time.sleep(1)
                    logger.info("Early stopping")
                    self.new_click(tuple_add(rect, self.locs.view_team))
                    self.new_click(tuple_add(rect, self.locs.give_up))
                    self.new_click(tuple_add(rect, self.locs.give_up_cfm))
                else:
                    self.new_click(tuple_add(rect, self.locs.start_game))
                self.surprise_relative_loc = None  # 漩涡已选择

            if state == 'visitor_list':
                logger.info(f'find {state}, try to click')
                _, screen = find_lushi_window(self.title)
                # advice = self.pick_visitor(screen)
                advice = self.choose_one_from_three(screen, "heros")
                t_id = random.choice(advice)
                visitor_loc = (self.locs.visitors[t_id], self.locs.visitors[-1])
                logger.info(f"click visitor : {t_id} at locs {visitor_loc}")
                self.new_click(tuple_add(rect, visitor_loc))

                time.sleep(1)  # 多次截屏没有 截住
                # visitor, pick mission record
                if self.debug or self.basic.screenshot_visitor:
                    screenshot(self.title, state)

                self.new_click(tuple_add(rect, self.locs.visitors_confirm))

                for _ in range(4):
                    self.new_click(tuple_add(rect, self.locs.empty))

                logger.info("Visitors Selected")
                self.surprise_relative_loc = None  # 漩涡已选择
                if self.basic.early_stop:
                    # 休眠2秒再退出，免得太卡导致失败
                    time.sleep(2)
                    logger.info("Early stopping")
                    self.new_click(tuple_add(rect, self.locs.view_team))
                    self.new_click(tuple_add(rect, self.locs.give_up))
                    self.new_click(tuple_add(rect, self.locs.give_up_cfm))

            if state in ['final_reward', 'final_reward2']:
                logger.info(f'find {state}, try to click')
                reward_count = self.basic.reward_count_dropdown
                reward_count = int(reward_count) if reward_count.isdigit() else reward_count

                reward_locs = eval(self.locs.rewards[reward_count])  # click all of 3， 4， 5 rewards location
                for loc in reward_locs:
                    pyautogui.moveTo(tuple_add(rect, loc))
                    self.new_click()

                # 现在宝藏有可能出双倍，点两次
                for loc in reward_locs:
                    pyautogui.moveTo(tuple_add(rect, loc))
                    self.new_click()

                if self.basic.screenshot_reward or self.debug:  # record reward by image
                    screenshot(self.title, state)

                pyautogui.moveTo(tuple_add(rect, self.locs.rewards['confirm']))
                self.new_click()

            if state == 'final_confirm':
                logger.info(f'find {state}, try to click')
                self.new_click(tuple_add(rect, self.locs.final_confirm))

        return success, tic, state, rect

    def run(self):
        if self.basic.auto_restart:
            while True:
                try:
                    self.run_pve()
                except AssertionError as e:
                    logger.error(f'错误：请删除炉石路径下的Logs/Power.log再重新打开!!!!')
                    break
                except Exception as e:
                    logger.error(f'错误：{e}', exc_info=True)
                    try:
                        if self.basic.screenshot_error:
                            screenshot(self.title, 'error')
                    except:
                        pass
                    restart_game(self.lang, self.basic.bn_path, False)
        else:
            self.run_pve()

    def run_pve(self):
        time.sleep(2)
        success, loc, rect = self.check_in_screen('mercenaries')
        tic = time.time()
        state = ""

        while True:
            if (rect is not None) and (self.locs.empty is not None):
                self.new_click(tuple_add(rect, self.locs.empty))
            else :
                # 不知为啥，最近开始报这个错误
                screenshot(self.title, 'restart_ract_noe')
                if self.basic.auto_restart:
                    restart_game(self.lang, self.basic.bn_path)
            if time.time() - tic > self.basic.longest_waiting:
                if self.basic.screenshot_error:
                    screenshot(self.title, 'restart_block')
                    if self.basic.auto_restart:
                        restart_game(self.lang, self.basic.bn_path)
                if state == 'not_ready_dots' or state == 'member_not_ready' or state == 'member_not_ready2':
                    pyautogui.rightClick(tuple_add(rect, self.locs.empty))
                    self.new_click(tuple_add(rect, self.locs.options))
                    self.new_click(tuple_add(rect, self.locs.surrender))
                elif state == 'map_not_ready':
                    self.new_click(tuple_add(rect, self.locs.view_team))
                    self.new_click(tuple_add(rect, self.locs.give_up))
                    self.new_click(tuple_add(rect, self.locs.give_up_cfm))
                else:
                    screenshot(self.title, 'restart_unkown')
                    if self.basic.auto_restart:
                        restart_game(self.lang, self.basic.bn_path)
                tic = time.time()
            else:
                logger.info("Last state %s, time taken: %.2f", state, time.time() - tic)

            for state_text in self.states:
                success, tic, state, rect = self.state_handler(state, tic, state_text)
                if success:
                    self.new_click(tuple_add(rect, self.locs.empty))


def run_from_gui(cfg):
    logger.debug(cfg)
    if cfg['lang'].startswith('EN'):
        lang = 'eng'
    elif cfg['lang'].startswith('ZH'):
        lang = 'chs'
    else:
        lang = None
    restart_game(lang, cfg['bn_path'], kill_existing=False)
    agent = Agent(cfg=cfg)
    agent.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=['chs', 'eng'], default='chs', help='Choose Your Hearthstone Language')
    parser.add_argument('--config', default='config/default.yaml', help='launch config filename')
    parser.add_argument('--func', choices=['run', 'coor'], help='Run main function or find coordinates')
    args = parser.parse_args()

    if args.func == 'run':
        with open(args.config, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)

        if args.lang == 'chs':
            cfg['lang'] = 'ZH-1600x900'
        else:
            cfg['lang'] = 'EN-1024x768'

        run_from_gui(cfg)
    elif args.func == 'coor':
        if args.lang == 'chs':
            title = '炉石传说'
        elif args.lang == 'eng':
            title = 'Hearthstone'
        else:
            title = None
        while True:
            find_relative_loc(title)
            time.sleep(1)


if __name__ == '__main__':
    main()
