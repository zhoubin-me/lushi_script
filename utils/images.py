import cv2
import numpy as np
from PIL import Image

def get_sub_image(screen, x1, y1, x2, y2):
    roiImg = screen[y1:y2, x1:x2]
    # img = Image.fromarray(roiImg)
    # img.save("test1.png")
    return roiImg 
