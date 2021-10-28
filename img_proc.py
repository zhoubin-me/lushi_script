
import cv2
import numpy as np
from util import find_lushi_window, find_icon_location
import time


def analyse_battle_field(region, screen, digits=None):
    x1, y1, x2, y2 = region
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    img = screen[y1:y2, x1:x2]
    if digits is None:
        digits = cv2.imread('imgs_chs_1600x900\\icons\\digits.png')
    cv2.imwrite('gray.png', img)
    print(screen.shape, region, digits.shape)
    _, thresh1 = cv2.threshold(img[:, :, 2], 251, 255, 0)
    _, thresh2 = cv2.threshold(img[:, :, 1], 251, 255, 0)
    thresh = cv2.bitwise_or(thresh1, thresh2)
    cv2.imwrite('gray_thr.png', thresh)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    img_copy = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    data = []
    print(stats)
    for i in range(1, num_labels):
        mask = labels == i
        x, y, w, h, a = stats[i]
        w, h = 17, 30
        if stats[i][-1] > 100:
            if x < 3 or y < 3:
                continue
            img_copy[:, :, 0][mask] = 255
            img_copy[:, :, 1][mask] = 255
            img_copy[:, :, 2][mask] = 255
            digit = img_copy[y-3:y+h, x-3:x+w]
            cv2.imwrite(f'digit_{i}.png', digit)
            success, x, y, conf = find_icon_location(digits, digit, 0.7)
            if success:
                data.append(list(stats[i][:-1]) + [conf, np.rint((x-14) / 28)])
                print(i, data[-1])
    cv2.imwrite('gray_copy.png', img_copy)
    data.sort(key=lambda e: e[0])
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
    assert(len(data_clean) % 2 == 0)
    N = len(data_clean) // 2
    output = []
    for i in range(N):
        damage, health = data_clean[2*i], data_clean[2*i+1]
        center_x = (damage[0] + damage[2] // 2 + health[0] + health[2] // 2) // 2
        center_y = (damage[1] + damage[3]) // 2 + 28
        color_region = img[center_y-5:center_y+5, center_x-10:center_x+10]
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
        hero_img = screen[hero_y-35:hero_y+35, hero_x-50:hero_x+50]
        output.append((i, hero_x, hero_y, int(damage[-1]), int(health[-1]), color))
        cv2.imwrite(f'hero_{i}.png', hero_img)
        print(B, G, R)
    print(output)
    return output


if __name__ == '__main__':
    time.sleep(1)
    rect, img = find_lushi_window("炉石传说", to_gray=False)
    region = [ 400, 293, 1230, 393]
    region2 = [ 400, 650, 1230, 750]
    analyse_battle_field(region2, img)
