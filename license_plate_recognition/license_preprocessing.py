import numpy as np
import cv2 as cv
import math


def license_getcontours(original_image):

    # 将一张RGB 图片转换为 HSV 图片格式
    hsv_image = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)
    # 获取h、s、v图片分量，图片h分量的shape
    h_split, s_split, v_split = cv.split(hsv_image)
    rows, cols = h_split.shape
    rows, cols
    # 2. 遍历图片，找出蓝色区域
    # 创建全黑背景。== 原始图片大小
    binary_image = np.zeros((rows, cols), dtype=np.uint8)
    # 设置感兴趣|提取的 颜色的 hsv 的区间 : 可调的经验值
    HSV_MIN_BLUE_H = 85
    HSV_MAX_BLUE_H = 150
    HSV_MIN_BLUE_SV = 70
    HSV_MAX_BLUE_SV = 255

    # 遍历图片的每一个像素， 找到满足条件(hsv找蓝色)的像素点，设置为255 ==binary_image中
    for row in np.arange(rows):
        for col in np.arange(cols):
            H = h_split[row, col]
            S = s_split[row, col]
            V = v_split[row, col]
            # 判断像素落在蓝色区域并满足 sv 条件
            if (H > HSV_MIN_BLUE_H and H < HSV_MAX_BLUE_H) and (S > HSV_MIN_BLUE_SV and S < HSV_MAX_BLUE_SV) and (
                    V > HSV_MIN_BLUE_SV and V < HSV_MAX_BLUE_SV):
                binary_image[row, col] = 255
    # # 灰度
    # gray_image=cv.cvtColor(binary_image,cv.COLOR_BGR2GRAY)
    # cv.imshow('gray_image', gray_image)
    # cv.waitKey()
    # cv.destroyAllWindows()
    # 二值化
    ret, binary_image = cv.threshold(binary_image, 0, 255, cv.THRESH_OTSU)
    # sobel算子
    # x方向
    sobel_x = cv.Sobel(binary_image, cv.CV_16S, 1, 0)
    abs_x = cv.convertScaleAbs(sobel_x)
    # y方向
    sobel_y = cv.Sobel(abs_x, cv.CV_16S, 0, 1)
    abs_y = cv.convertScaleAbs(sobel_y)
    dst = cv.addWeighted(abs_x, 0.5, abs_y, 0.2, 0)
    # 自适应阈值
    ret, adapt_image = cv.threshold(dst, 0, 255, cv.THRESH_OTSU)
    # 闭运算
    kenerlX = cv.getStructuringElement(cv.MORPH_RECT, (10, 1))
    image = cv.morphologyEx(adapt_image, cv.MORPH_CLOSE, kenerlX, iterations=1)
    # 腐蚀与膨胀
    kernelX = cv.getStructuringElement(cv.MORPH_RECT, (20, 1))  # 25 1
    kernelY = cv.getStructuringElement(cv.MORPH_RECT, (1, 20))

    image = cv.dilate(image, kernelX, iterations=2)
    image = cv.erode(image, kernelX, iterations=3)  # 4
    image = cv.dilate(image, kernelX, iterations=2)

    image = cv.erode(image, kernelY, iterations=1)
    image = cv.dilate(image, kernelY, iterations=1)
    # 中值滤波去除噪点，平滑处理
    image = cv.medianBlur(image, 3)
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    origin_copy = original_image.copy()
    cv.drawContours(origin_copy, contours, -1, (0, 0, 255))  # 在原图上绘制
    return contours


def license_locate(original_image, contours):
    res_contours = []
    original_copy = original_image.copy()
    candidate_regions = []
    for i in np.arange(len(contours)):
        x, y, w, h = cv.boundingRect(contours[i])
        ratio = w * 1.0 / h
        # 处理长宽比
        if ratio < 1:
            ratio = 1.0 / ratio
        area = w * h
        if area > 1500 and area < 136 * 36 * 100 and ratio > 2.0 and ratio <= 5.0:  # 136*36：经验值，关键看radio比例
            candidate_regions.append(original_copy[y:y + h, x:x + w])
            res_contours.append(contours[i])

    return res_contours, candidate_regions


def license_rotate(original_image, res_contours):
    cnt = res_contours

    image = original_image.copy()
    [dx, dy, x, y] = cv.fitLine(cnt, cv.DIST_L2, 0, 0.01, 0.01)
    k = dy / dx
    b = y - k * x
    # 获取角度
    angle = math.atan(k)
    angle = math.degrees(angle)

    # 图像旋转
    h = image.shape[0]
    w = image.shape[1]
    # 旋转
    rotate_image = cv.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    rotate_image = cv.warpAffine(image, rotate_image, (int(w * 1.1), int(h * 1.1)))

    return rotate_image

def find_waves(threshold, histogram):
    """ 根据设定的阈值和图片直方图，找出波峰，用于分隔字符 """
    up_point = -1  # 上升点
    is_peak = False
    if histogram[0] > threshold:
        up_point = 0
        is_peak = True
    wave_peaks = []
    for i, x in enumerate(histogram):
        if is_peak and x < threshold:
            if i - up_point > 2:
                is_peak = False
                wave_peaks.append((up_point, i))
        elif not is_peak and x >= threshold:
            is_peak = True
            up_point = i
    if is_peak and up_point != -1 and i - up_point > 4:
        wave_peaks.append((up_point, i))
    return wave_peaks



def remove_upanddown_border(img):
    """ 去除车牌上下无用的边缘部分，确定上下边界 """
    row_histogram = np.sum(img, axis=1)  # 数组的每一行求和
    row_min = np.min(row_histogram)
    row_average = np.sum(row_histogram) / img.shape[0]
    row_threshold = (row_min + row_average) / 2
    wave_peaks = find_waves(row_threshold, row_histogram)
    # 挑选跨度最大的波峰
    wave_span = 0.0
    for wave_peak in wave_peaks:
        span = wave_peak[1] - wave_peak[0]
        if span > wave_span:
            wave_span = span
            selected_wave = wave_peak
    plate_binary_img = img[selected_wave[0]:selected_wave[1], :]
    return plate_binary_img


def find_end(start, arg, black, white, width, black_max, white_max, isfirst, length):
    if isfirst:
        return start + length
    end = start + 1
    for m in range(start + 1, width - 1):
        if (black[m] if arg else white[m]) > (0.85 * black_max if arg else 0.85 * white_max):
            end = m
            break
    return end


def char_segmentation(thresh):
    """ 分割字符 """
    white, black = [], []  # list记录每一列的黑/白色像素总和
    height, width = thresh.shape
    white_max = 0  # 仅保存每列，取列中白色最多的像素总数
    black_max = 0  # 仅保存每列，取列中黑色最多的像素总数
    # 计算每一列的黑白像素总和
    for i in range(width):
        line_white = 0  # 这一列白色总数
        line_black = 0  # 这一列黑色总数
        for j in range(height):
            if thresh[j][i] == 255:
                line_white += 1
            if thresh[j][i] == 0:
                line_black += 1
        white_max = max(white_max, line_white)
        black_max = max(black_max, line_black)
        white.append(line_white)
        black.append(line_black)
    # arg为true表示黑底白字，False为白底黑字
    arg = True
    if black_max < white_max:
        arg = False

    # 分割车牌字符
    n = 1
    flag = True
    cropImgs = []
    k = 0
    length = 20
    while n <= width - 2:
        n += 1
        # 判断是白底黑字还是黑底白字  0.05参数对应上面的0.95 可作调整
        if (white[n] if arg else black[n]) > (0.15 * white_max if arg else 0.15 * black_max):  # 这点没有理解透彻
            if (len(cropImgs) != 0):
                flag = False
            start = n
            if (k == 6):
                length = min(width - start - 5, 15)
                flag = True
            end = find_end(start, arg, black, white, width, black_max, white_max, flag, length)
            n = end
            if end - start >= 4 : # or end > (width * 3 / 7)
                k += 1
                cropImg = thresh[:, max(0, start - 4):min(width - 1, end + 4)]
                cropImg = cv.resize(cropImg, (32, 32))
                cropImgs.append(cropImg)

    return cropImgs


def license_split(raw_image):
    # 统一车牌大小
    # 声明统一的尺寸
    PLATE_STD_HEIGHT = 60
    PLATE_STD_WIDTH = 160
    # 完成 resize
    uniformed_image = cv.resize(raw_image, (PLATE_STD_WIDTH, PLATE_STD_HEIGHT))
    # cv.imshow("uniformed_image", uniformed_image)
    # cv.waitKey()
    # cv.destroyAllWindows()
    # 灰度处理
    gray_image = cv.cvtColor(uniformed_image, cv.COLOR_RGB2GRAY)
    # cv.imshow("gray_image", gray_image)
    # cv.waitKey()
    # cv.destroyAllWindows()
    # 自适应阈值
    ret, binary_image = cv.threshold(gray_image, 0, 255, cv.THRESH_OTSU)
    plate_binary_img = remove_upanddown_border(binary_image)
    # cv.imshow('plate_binary_img', plate_binary_img)
    # cv.waitKey()
    # cv.destroyAllWindows()
    cropImgs = char_segmentation(plate_binary_img)
    return cropImgs
