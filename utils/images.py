import numpy as np
from PIL import Image

def get_sub_np_array(np_array, x1, y1, x2, y2):
    roiImg = np_array[y1:y2, x1:x2]
    # img = Image.fromarray(roiImg)
    # img.save("test1.png")
    return roiImg 
