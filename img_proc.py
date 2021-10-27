
import cv2
import numpy as np
from util import find_lushi_window

def analyse_battle_field(region, screen):
    cv2.imwrite('')
    x1, y1, x2, y2 = region
    img = screen[x1:x2, y1:y2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(img_gray, 250, 255, 0)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    img_copy = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    # print(stats)
    for i in range(1, num_labels):
        mask = labels == i
        if stats[i][-1] > 50:
            img_copy[:, :, 0][mask] = 255
            img_copy[:, :, 1][mask] = 255
            img_copy[:, :, 2][mask] = 255


if __name__ == '__main__':
    rect, img = find_lushi_window("炉石传说")
    region = [ 400, 300, 1230, 400 ]
    analyse_battle_field(region, img)