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
    for img in images:
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

# 获取图中闪亮的绿色圆圈, 55, 110
def get_burning_green_circles(img, minRad = 55, maxRad = 110, withBlue = True):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imwrite("test_origin11.png", img)

    if withBlue:
        lower_blue = np.array([108, 65, 65])
        upper_blue = np.array([120, 255, 255])
        mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
        res2 = cv2.bitwise_and(img, img, mask=mask2)
        # cv2.imwrite("tetsts11_blue.png", res2)

    # define range of burning green color in HSV
    lower_green = np.array([55, 50, 50])
    upper_green = np.array([75, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    dts = None
    if withBlue:
        dst = cv2.addWeighted(res, 0.5, res2, 0.5, 0)   # 图片组合
    else:
        dst = res

    gay_img = cv2.cvtColor(dst, cv2.COLOR_BGRA2GRAY)
    the_img = cv2.blur(gay_img, (4, 4))  # 模糊，去噪点
    circles = cv2.HoughCircles(the_img, cv2.HOUGH_GRADIENT, 1, 35,
                               param1=100, param2=30, minRadius=minRad, maxRadius=maxRad)
    if circles is None:
        return []
    
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:  # 遍历矩阵每一行的数据
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imwrite("gar_img111_green.png", img) # TODO remove before submit
    return circles


# 获取图中闪亮的蓝色直线
def get_burning_blue_lines(img, minRad = 10, maxRad = 100):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 65, 65])
    upper_blue = np.array([125, 255, 255])
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    canney_edges = cv2.Canny(res2,100,200) # 检查出 高亮边缘

    lines = cv2.HoughLines(canney_edges,1,np.pi/180,200)
    if lines is None:
        return []
    
    # for line in lines:
    #     rho,theta = line[0]
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a*rho
    #     y0 = b*rho
    #     x1 = int(x0 + 1000*(-b))
    #     y1 = int(y0 + 1000*(a))
    #     x2 = int(x0 - 1000*(-b))
    #     y2 = int(y0 - 1000*(a))
    #     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    # cv2.imwrite("gar_img111.png", img)

    return lines