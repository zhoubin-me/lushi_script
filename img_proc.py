
import cv2
import numpy as np
from util import find_lushi_window
import time
import pytesseract
import os

def analyse_battle_field(region, screen):
    pytesseract.pytesseract.tesseract_cmd = os.path.join("C:\\", "Program Files", "Tesseract-OCR", "tesseract.exe")
    x1, y1, x2, y2 = region
    screen =  cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    img = screen[y1:y2, x1:x2]
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.png', img)
    _, thresh1 = cv2.threshold(img[:, :, -1], 250, 255, 0)
    _, thresh2 = cv2.threshold(img[:, :, 1], 250, 255, 0)
    thresh = cv2.bitwise_or(thresh1, thresh1)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    img_copy = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    coords = []
    for i in range(1, num_labels):
        mask = labels == i
        if stats[i][-1] > 100:
            img_copy[:, :, 0][mask] = 255
            img_copy[:, :, 1][mask] = 255
            img_copy[:, :, 2][mask] = 255
            coords.append(list(stats[i]))
    img_data = pytesseract.image_to_boxes(img_copy, config='--oem 3 -c tessedit_char_whitelist={0123456789}')
    img_data_lines = img_data.split('\n')[:-1]
    coords = sorted(coords, key=lambda x: x[0])
    assert(len(img_data_lines) == len(coords))
    out = []
    numbers = []
    for i, coor in enumerate(coords):
        digit = int(img_data_lines[i][0])
        if i == 0:
            out.append(coor)
            numbers.append(digit)
        else:
            if np.abs(coor[0] - coords[i-1][0]) < 30:
                out[-1][2] = np.abs(coor[0] - coords[i-1][0]) + coor[2]
                numbers[-1] = numbers[-1] * 10 + digit
            else:
                out.append(coor)
                numbers.append(digit)
    print(out)
    assert(len(out) % 2 == 0)
    N = len(out) // 2

    data = {}
    for i in range(N):
        x, y = (out[2*i][0] + out[2*i][2]//2 + out[2*i+1][0] + out[2*i+1][2]//2) // 2, out[2*i][1] + out[2*i][3] // 2 + 12
        region = img[y-5:y+5, x-10:x+10]
        cv2.imwrite(f'digit{i}.png', region)
        B, G, R = region[:, :, 0].mean(), region[:, :, 1].mean(), region[:, :, 2].mean()
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

        data[i] = (x + x1, y + y1-50, color, numbers[2*i], numbers[2*i+1])

        print(B, G, R)
    print(data)
    return data
    

if __name__ == '__main__':
    time.sleep(1)
    rect, img = find_lushi_window("炉石传说", to_gray=False)
    region = [ 355, 180, 1250, 374 ]
    analyse_battle_field(region, img)