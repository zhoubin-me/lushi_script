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

PLATFORM = platform.system()

HEROS = {'LETL_009H_01': ['格罗玛什·地狱咆哮', 'Grommash Hellscream'],
         'LETL_006H_01': ['加拉克苏斯大王', 'Lord Jaraxxus'],
         'BARL_005H_02': ['沃金', "Vol'jin"],
         'LETL_012H_01': ['瓦里安·乌瑞恩', 'Varian Wrynn'],
         'LETL_024H_01': ['尤朵拉', 'Eudora'],
         'LETL_032H_01': ['光明之翼', 'Brightwing'],
         'LETL_037H_01': ['暴龙王克鲁什', 'King Krush'],
         'LETL_030H_01': ['迦顿男爵', 'Baron Geddon'],
         'SWL_26H_03': ['迪亚波罗', 'Diablo'],
         'LETL_040H_01': ['塔姆辛·罗姆', 'Tamsin Roame'],
         'LETL_036H_01': ['古夫·符文图腾', 'Guff Runetotem'],
         'BARL_025H_01': ['萨尔', 'Thrall'],
         'LETL_014H_01': ['先知维伦', 'Prophet Velen'],
         'LETL_811H': ['厨师曲奇', 'Cooki'],
         'BARL_007H_01': ['安娜科德拉', 'Lady Anacondra'],
         'LETL_038H_02': ['穆克拉', 'King Mukla'],
         'LETL_015H_01': ['雷克萨', 'Rexxar'],
         'SWL_01H_01': ['安东尼达斯', 'Antonidas'],
         'LETL_034H_01': ['凯恩·血蹄', 'Cairne Bloodhoof'],
         'SWL_10H_02': ['安度因·乌瑞恩', 'Anduin Wrynn'],
         'LETL_028H_02': ['拉格纳罗斯', 'Ragnaros'],
         'LT21_01H_01': ['艾德温，迪菲亚首脑', 'Edwin, Defias Kingpin'],
         'SWL_13H_01': ['乌瑟尔', 'Uther'],
         'BARL_010H_03': ['古尔丹', "Gul'dan"],
         'BARL_017H_01': ['玛法里奥·怒风', 'Malfurion Stormrage'],
         'LETL_020H_01': ['凯瑞尔·罗姆', 'Cariel Roame'],
         'BARL_024H_01': ['剑圣萨穆罗', 'Blademaster Samuro'],
         'BARL_008H_02': ['穆坦努斯', 'Mutanus'],
         'LETL_029H_01': ['布鲁坎', "Bru'kan"],
         'BARL_023H_01': ['拉索利安', 'Rathorian'],
         'LETL_027H_02': ['神谕者摩戈尔', 'Morgl the Oracle'],
         'BARL_009H_01': ['指挥官沃恩', 'War Master Voone'],
         'LT21_03H_01': ['斯尼德', 'Sneed'],
         'BARL_002H_01': ['萨鲁法尔', 'Saurfang'],
         'LETL_001H_02': ['希尔瓦娜斯·风行者', 'Sylvanas Windrunner'],
         'SWL_25H_01': ['吉安娜·普罗德摩尔', 'Jaina Proudmoore'],
         'LETL_010H_01': ['斯卡布斯·刀油', 'Scabbs Cutterbutter'],
         'BARL_013H_01': ['加尔鲁什·地狱咆哮', 'Garrosh Hellscream'],
         'LT21_04H_01': ['重拳先生', 'Mr. Smite'], 'LETL_039H_02': ['塔维什·雷矛', 'Tavish Stormpike'],
         'BARL_016H_01': ['泰兰德', 'Tyrande'],
         'LETL_005H_01': ['米尔豪斯·法力风暴', 'Millhouse Manastorm'],
         'LETL_031H_02': ['阿莱克丝塔萨', 'Alexstrasza'],
         'LETL_011H_01': ['娜塔莉·塞林', 'Natalie Seline'],
         'BARL_012H_01': ['玛诺洛斯', 'Mannoroth'],
         'LETL_016H_02': ['洛卡拉', 'Rokara'],
         'LETL_021H_02': ['泽瑞拉', 'Xyrella'],
         'LETL_002H_02': ['提里奥·弗丁', 'Tirion Fordring'],
         'LETL_041H_03': ['巫妖王', 'The Lich King'],
         'LETL_007H_01': ['库尔特鲁斯·陨烬', 'Kurtrus Ashfallen'],
         'LETL_033H_01': ['格鲁尔', 'Gruul'],
         'SWL_06H_01': ['考内留斯·罗姆', 'Cornelius Roame'],
         'LETL_017H_01': ['瓦尔登·晨拥', 'Varden Dawngrasp'],
         'SWL_14H_02': ['闪狐', 'Blink Fox'],
         'LETL_003H_02': ['伊利丹·怒风', 'Illidan Stormrage'],
         'LETL_026H_01': ['老瞎眼', 'Old Murk-Eye']}



if PLATFORM:
    import win32gui
    from winguiauto import findTopWindow


    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


    def set_top_window(title):
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
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
        if len(p.name()) > 0 and p.name() in process_names:
            print(f"find {p.name()} exists")
            return True
    return False


def proc_kill(process_names):
    for p in psutil.process_iter():
        if len(p.name()) > 0 and p.name() in process_names:
            p.kill()
            print(f"{p.name()} killed")


def restart_game(lang, battle_net_path):
    bn = 'Battle.net.exe'
    hs = 'Hearthstone.exe'
    # battle_net_path = os.path.join(*battle_net_path)
    if lang == 'eng':
        title = 'Hearthstone'
    elif lang == 'chs':
        title = "炉石传说"
    else:
        raise ValueError(f"Language {lang} not supported")

    proc_kill([bn, hs])

    time.sleep(5)
    while not proc_exist(bn):
        print('attempt to start Battle.net')
        win32api.ShellExecute(0, 'open', battle_net_path,
                              '--exec=\"launch WTCG\"',
                              '', 1)
        time.sleep(10)

    print('Battle.net start success')

    while not proc_exist(hs):
        print('attempt to start Hearthstone')
        win32api.ShellExecute(0, 'open', battle_net_path,
                              '--exec=\"launch WTCG\"',
                              '', 1)
        time.sleep(10)
    print('Hearthstone start success')
    time.sleep(5)
    set_top_window(title)
    print('done')


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
    # restart_game("chs")
    a = 'C:\\Program Files (x86)\\Battle.net\\Battle.net.exe'
    restart_game('chs', a)
    # BattleAi.battle(None, None)
