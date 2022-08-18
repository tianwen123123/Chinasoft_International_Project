import numpy as np
import tensorflow as tf
import cv2 as cv
import math

def load_datasets_license():
    # 初始化设置图片文件位置
    original_file_path = 'images/A82806.jpg'
    original_image = cv.imread(original_file_path)

    return original_image