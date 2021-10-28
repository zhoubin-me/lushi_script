import cv2
import pyautogui
from PIL import ImageGrab, Image
import numpy as np
import platform
import psutil
import os
import time
import win32api

PLATFORM = platform.system()

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
        if p.name() in process_names:
            print(f"find {p.name()} exists")
            return True
    return False


def proc_kill(process_names):
    for p in psutil.process_iter():
        if p.name() in process_names:
            p.kill()
            print(f"{p.name()} killed")


def restart_game(lang, battle_net_path):
    bn = 'Battle.net.exe'
    hs = 'Hearthstone.exe'
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
    set_top_window(title)
    print('done')


if __name__ == "__main__":
    # restart_game("chs")
    a = 'C:\\Program Files (x86)\\Battle.net\\Battle.net.exe'
    restart_game('chs', a)
