import numpy as np
from PIL import Image
import cv2
from utils.img_match import Stitcher


def get_sub_np_array(np_array, x1, y1, x2, y2):
    roiImg = np_array[y1:y2, x1:x2]
    # img = Image.fromarray(roiImg) # TODO check before commit
    # img.save("test1.png")
    return roiImg


def img_rotaion(img, left=True):
    return np.rot90(img, 3)
    # 获取输入图像的信息，生成旋转操作所需的参数（padding: 指定零填充的宽度； canter: 指定旋转的轴心坐标）
    h, w = img.shape[:2]
    padding = (w - h) // 2
    center = (w // 2, w // 2)

    # 在原图像两边做对称的零填充，使得图片由矩形变为方形
    img_padded = np.zeros(shape=(w, w, 3), dtype=np.uint8)
    img_padded[padding:padding+h, :, :] = img

    # cv2.imshow("", img_padded)
    # cv2.waitKey(1000)
    # cv2.imwrite("./img_padded.jpg", img_padded)

    # 逆时针-90°(即顺时针90°)旋转填充后的方形图片
    M = cv2.getRotationMatrix2D(center, -90, 1)
    rotated_padded = cv2.warpAffine(img_padded, M, (w, w))

    # cv2.imshow("", rotated_padded)
    # cv2.waitKey(1000)
    # cv2.imwrite("./rotated_padded.jpg", rotated_padded)

    # 从旋转后的图片中截取出我们需要的部分，作为最终的输出图像
    output = rotated_padded[:, padding:padding+h, :]

    # cv2.imshow("", output)
    # cv2.waitKey(1000)
    # cv2.imwrite("./output.jpg", output)
    return output

def images_to_full_map(images):
    # imagePaths.reverse()
    first = None
    second = None
    result = None
    i = 0
    for img in images :
        i = i + 1
        if 1 == i:
            first = img
            continue
        else:
            second = img

        if (first is not None and second is not None):
            # 把图像叠合在一起以构建全景图
            stitcher = Stitcher()
            (result, vis) = stitcher.stitch([first, second], showMatches=True)
            # 展示图像
            # cv2.imshow("Keypoint Matches", vis)
            # cv2.imwrite("res" + str(i) + ".jpg", result)
            first = result

        del second
    
    return result