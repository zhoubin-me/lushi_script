
import cv2
import numpy as np
from util import find_lushi_window, find_icon_location
import time


def analyse_battle_field(region, screen, digits):
    x1, y1, x2, y2 = region
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    img = screen[y1:y2, x1:x2]
    _, thresh1 = cv2.threshold(img[:, :, 2], 250, 255, 0)
    _, thresh2 = cv2.threshold(img[:, :, 1], 250, 255, 0)
    thresh = cv2.bitwise_or(thresh1, thresh2)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    img_copy = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    cv2.imwrite('img_crop.png', img)
    cv2.imwrite('img_thr.png', thresh)
    data = []
    print(stats)
    for i in range(1, num_labels):
        x, y, w, h, a = stats[i]
        w, h = 17, 30
        if stats[i][-1] > 50:
            if x < 3 or y < 3:
                continue
            img_ = np.zeros((img.shape[0], img.shape[1]), np.uint8)
            img_[labels == i] = 255
            digit = img_[y-3:y+h, x-3:x+w]
            # cv2.imwrite(f'digit_{i}.png', digit)
            success, x, y, conf = find_icon_location(digits, digit, 0.7)
            # print(i, list(stats[i][:-1]), conf, a)
            if success:
                data.append(list(stats[i][:-1]) + [conf, np.rint((x-14) / 28)])
                img_copy[labels == i] = 255
                # (i, data[-1])
    data.sort(key=lambda e: e[0])
    cv2.imwrite('img_clean.png', img_copy)
    print(data)
    data_clean = []
    for i, entry in enumerate(data):
        if i == 0:
            data_clean.append(entry)
        else:
            x_diff = entry[0] - data_clean[-1][0]
            if np.abs(x_diff) < 40:
                data_clean[-1][2] = x_diff + entry[2]
                data_clean[-1][-1] = data_clean[-1][-1] * 10 + entry[-1]
            else:
                data_clean.append(entry)
    assert(len(data_clean) % 2 == 0)
    N = len(data_clean) // 2
    output = []
    for i in range(N):
        damage, health = data_clean[2*i], data_clean[2*i+1]
        center_x = (damage[0] + damage[2] // 2 + health[0] + health[2] // 2) // 2
        center_y = (damage[1] + damage[3]) // 2 + 28
        color_region = img[center_y-5:center_y+5, center_x-10:center_x+10]
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
        hero_img = screen[hero_y-35:hero_y+35, hero_x-50:hero_x+50]
        output.append((i, hero_x, hero_y, int(damage[-1]), int(health[-1]), color))
    print(output)
    return output


def concate():
    img = np.zeros((33, 280), dtype=np.uint8)
    for i in range(10):
        im = cv2.cvtColor(cv2.imread(f'{i}.png'), cv2.COLOR_BGR2GRAY)
        img[:, 4+i*28:24+i*28] = im

    cv2.imwrite('digits.png', img)

if __name__ == '__main__':
    time.sleep(1)
    concate()
    rect, img = find_lushi_window("hearthstone", to_gray=False)
    digits = cv2.cvtColor(cv2.imread('imgs_eng_1024x768\\icons\\digits.png'), cv2.COLOR_BGR2GRAY)
    enemy_region = [200, 260, 888, 348]  # [x1, y1, x2, y2]
    hero_region = [200, 571, 888, 659]
    hero_nready_region = [200, 480, 888, 568]
    analyse_battle_field(enemy_region, img, digits)
