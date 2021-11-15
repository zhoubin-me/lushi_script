import logging
import sys
from datetime import datetime

import cv2
import pyautogui
from PIL import ImageGrab, Image
import numpy as np
import platform
import os
import psutil
import time
import win32api
from PyQt5.QtWidgets import *
import csv
import utils.logging_util

logger = logging.getLogger()

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PLATFORM = platform.system()


def read_hero_data():
    main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(main_path, 'resource', 'hero_data.csv')
    heros = {}
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count > 0:
                # print(row)
                num_id, name_eng, race, name_chs, sn_id, damage1, target1, speed1, type1, others1, \
                damage2, target2, speed2, type2, others2, \
                damage3, target3, speed3, type3, others3 = row

                spells = {
                    0: {'damage': int(damage1) if len(damage1) else 0, 'range': target1, 'speed': speed1, 'type': type1,
                        'others': others1},
                    1: {'damage': int(damage2) if len(damage2) else 0, 'range': target2, 'speed': speed2, 'type': type2,
                        'others': others2},
                    2: {'damage': int(damage3) if len(damage3) else 0, 'range': target3, 'speed': speed3, 'type': type3,
                        'others': others3},
                }

                heros[sn_id[:-3]] = [name_chs, name_eng[1:-1], race[1:-1], spells]
            count += 1
    return heros


HEROS = read_hero_data()

if PLATFORM:
    import win32gui
    from utils.winguiauto import findTopWindow


    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


    def set_top_window(title):
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        title = title.lower()
        for i in top_windows:
            if title in i[1].lower():
                win32gui.ShowWindow(i[0], 5)
                win32gui.SetForegroundWindow(i[0])
                return True
        else:
            return False


    def find_lushi_window(title, to_gray=True):
        hwnd = findTopWindow(title)
        rect = win32gui.GetWindowPlacement(hwnd)[-1]
        image = ImageGrab.grab(rect)
        if to_gray:
            image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        else:
            image = np.array(image)
        return rect, image


    def screenshot(title, file_name=None):
        hwnd = findTopWindow(title)
        rect = win32gui.GetWindowPlacement(hwnd)[-1]
        image = ImageGrab.grab(rect)
        dt = datetime.strftime(datetime.now(), "%Y-%m-%d_%H")
        screenshot_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', dt, 'screenshot')
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        if file_name is None:
            file_name = datetime.strftime(datetime.now(), '%H.%M.%S,%f')[:-3] + '.png'
        full_file_name = os.path.join(screenshot_path, file_name)
        image.save(full_file_name)
        logger.info(f'screenshot saved at {full_file_name}')



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
    del result
    if maxVal > confidence:
        (startX, startY) = maxLoc
        endX = startX + icon.shape[1]
        endY = startY + icon.shape[0]
        return True, (startX + endX) // 2, (startY + endY) // 2, maxVal
    else:
        return False, None, None, maxVal


def find_relative_loc(title='炉石传说'):
    pos = pyautogui.position()
    rect, _ = find_lushi_window(title)
    print((pos[0] - rect[0], pos[1] - rect[1]))


def move2loc(x, y, title='炉石传说'):
    rect, _ = find_lushi_window(title)
    loc = (x + rect[0], y + rect[1])
    pyautogui.moveTo(loc)


def proc_exist(process_names):
    for p in psutil.process_iter():
        try:
            if len(p.name()) > 0 and p.name() in process_names:
                logger.info(f"find {p.name()} exists")
                return True
        except Exception as e:
            logger.info(f"can not get name of process {e}")
    return False


def proc_kill(process_names):
    for p in psutil.process_iter():
        if len(p.name()) > 0 and p.name() in process_names:
            p.kill()
            logger.info(f"{p.name()} killed")


def restart_game(lang, battle_net_path, kill_existing=True):
    bn = 'Battle.net.exe'
    hs = 'Hearthstone.exe'
    if lang == 'eng':
        title = 'Hearthstone'
    elif lang == 'chs':
        title = "炉石传说"
    else:
        raise ValueError(f"Language {lang} not supported")
    if kill_existing:
        proc_kill([hs])
        time.sleep(5)

    while not proc_exist(bn):
        logger.info('attempt to start Battle.net')
        win32api.ShellExecute(0, 'open', battle_net_path,
                              '--exec=\"launch WTCG\"',
                              '', 1)
        time.sleep(10)

    logger.info('Battle.net start success')

    while not proc_exist(hs):
        logger.info('attempt to start Hearthstone')
        win32api.ShellExecute(0, 'open', battle_net_path,
                              '--exec=\"launch WTCG\"',
                              '', 1)
        time.sleep(10)
    logger.info('Hearthstone start success')
    time.sleep(5)
    set_top_window(title)
    logger.info('done')


def analyse_battle_field(region, screen, digits):
    x1, y1, x2, y2 = region
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    img = screen[y1:y2, x1:x2]
    cv2.imwrite('gray.png', img)
    _, thresh1 = cv2.threshold(img[:, :, 2], 250, 255, 0)
    _, thresh2 = cv2.threshold(img[:, :, 1], 250, 255, 0)
    thresh = cv2.bitwise_or(thresh1, thresh2)
    cv2.imwrite('gray_thr.png', thresh)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    img_copy = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    data = []
    print(stats)
    for i in range(1, num_labels):
        mask = labels == i
        x, y, w, h, a = stats[i]
        w, h = 17, 30
        if stats[i][-1] > 100:
            if x < 3 or y < 3:
                continue
            img_copy[mask] = 255
            digit = img_copy[y - 3:y + h, x - 3:x + w]
            cv2.imwrite(f'digit_{i}.png', digit)
            success, x, y, conf = find_icon_location(digits, digit, 0.7)
            data.append(list(stats[i][:-1]) + [conf, np.rint((x - 14) / 28)])
    cv2.imwrite('gray_copy.png', img_copy)
    data.sort(key=lambda e: e[0])
    print(data)
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
    output = []
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
        output.append((hero_x, hero_y, int(damage[-1]), int(health[-1]), color))
        cv2.imwrite(f'hero_{i}.png', screen[hero_y - 35:hero_y + 35, hero_x - 50:hero_x + 50])
        print(B, G, R)
    print(output)
    return output


def tuple_add(x, y):
    return x[0] + y[0], x[1] + y[1]


class DropLineEdit(QLineEdit):  # support drag
    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        # self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasText():
            file_path = e.mimeData().text()
            file_path = file_path.split('\n')
            # print(filePath[0])  # only read the first file
            file_path = file_path[0].split('///')  # remove file:///
            self.setText(file_path[1])  # save file path into QLineEdit
        else:
            e.ignore()


if __name__ == "__main__":
    screenshot_folder = r'resource\screenshot'
    screenshot('hearthstone', os.path.join(screenshot_folder))
