import cv2 as cv
import numpy as np
import math


def preprocessing(p1s, p2s, i, img):
    # 左上
    left_up = p1s[i]
    # 右下
    right_down = p2s[i]

    width = right_down[0] - left_up[0]
    height = right_down[1] - left_up[1]

    # 右上
    right_up = []
    right_up.append(right_down[0])
    right_up.append(left_up[1])

    # 左下
    left_down = []
    left_down.append(left_up[0])
    left_down.append(right_down[1])

    # pts1 是倾斜的图片的四个点的坐标
    pts1 = np.float32([left_up, right_up, left_down, right_down])
    # pts2 是处理后的四个点的坐标【下面】分别是 [左上]、[右上]、[左下]、[右下]
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    warped = cv.warpPerspective(img, M, (width, height))
    warped = cv.resize(warped, [148, 49, ])

    # 将一张RGB 图片转换为 HSV 图片格式
    hsv_image = cv.cvtColor(warped, cv.COLOR_BGR2HSV)
    # 获取h、s、v图片分量，图片h分量的shape
    h_split, s_split, v_split = cv.split(hsv_image)
    rows, cols = h_split.shape
    rows, cols
    # 2. 遍历图片，找出蓝色区域
    # 创建全黑背景。== 原始图片大小
    binary_image = np.zeros((rows, cols), dtype=np.uint8)
    # 设置感兴趣|提取的 颜色的 hsv 的区间 : 可调的经验值
    HSV_MIN_BLUE_H = 100
    HSV_MAX_BLUE_H = 150
    HSV_MIN_BLUE_SV = 85
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

    # 腐蚀与膨胀
    kernelX = cv.getStructuringElement(cv.MORPH_RECT, (7, 1))  # 25 1
    kernelY = cv.getStructuringElement(cv.MORPH_RECT, (1, 7))

    image = cv.dilate(binary_image, kernelX, iterations=1)
    image = cv.dilate(image, kernelY, iterations=2)
    # 中值滤波去除噪点，平滑处理
    image = cv.medianBlur(image, 3)
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # 获取轮廓
    origin_copy = warped.copy()
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(origin_copy, contours, -1, (0, 0, 255))  # 在原图上绘制

    # 获取车牌各个位置坐标
    # 获取第0个轮廓
    if (len(contours) == 0):
        return []
    contour = contours[0]
    rect = cv.minAreaRect(contour)
    box = cv.boxPoints(rect)
    box = np.int0(box)

    # 先取横坐标最小的两个
    left_index1 = 0  # 最小的
    left_index2 = 1
    left_min1 = box[0][0]
    left_min2 = box[1][0]

    if left_min1 > left_min2:
        temp = left_min1
        left_min1 = left_min2
        left_min2 = temp

        temp_index = left_index1
        left_index1 = left_index2
        left_index2 = temp_index

    if box[2][0] < left_min2:
        if box[2][0] < left_min1:
            left_index2 = left_index1
            left_index1 = 2
            left_min2 = left_min1
            left_min1 = box[2][0]
        else:
            left_index2 = 2
            left_min2 = box[2][0]

    if box[3][0] < left_min2:
        if box[3][0] < left_min1:
            left_index2 = left_index1
            left_index1 = 3
            left_min2 = left_min1
            left_min1 = box[3][0]
        else:
            left_index2 = 3
            left_min2 = box[3][0]
    # 左边
    if box[left_index1][1] < box[left_index2][1]:
        left_up = box[left_index1]
        left_down = box[left_index2]
    else:
        left_up = box[left_index2]
        left_down = box[left_index1]
    # 右边
    right_index1 = -1
    right_index2 = -1
    for i in range(4):
        if i != left_index1 and i != left_index2:
            if right_index1 == -1:
                right_index1 = i
            else:
                right_index2 = i
    if box[right_index1][1] < box[right_index2][1]:
        right_up = box[right_index1]
        right_down = box[right_index2]
    else:
        right_up = box[right_index2]
        right_down = box[right_index1]
    # 处理后的图片的宽和高
    width, height = 200, 60
    # pts1 是倾斜的图片的四个点的坐标
    pts1 = np.float32([left_up, right_up, left_down, right_down])
    # pts2 是处理后的四个点的坐标【下面】分别是 [左上]、[右上]、[左下]、[右下]
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    M = cv.getPerspectiveTransform(pts1, pts2)
    warped = cv.warpPerspective(origin_copy, M, (width, height))

    return warped


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
    length = 19

    while n <= width - 2:
        n += 1
        # 判断是白底黑字还是黑底白字  0.05参数对应上面的0.95 可作调整
        if (white[n] if arg else black[n]) > (0.10 * white_max if arg else 0.10 * black_max):  # 这点没有理解透彻
            if (len(cropImgs) != 0 and len(cropImgs) != 1):
                flag = False
            start = n
            if (k == 6):
                length = min(width - start - 5, 15)
                flag = True
            end = find_end(start, arg, black, white, width, black_max, white_max, flag, length)
            if end - start >= 4:  # or end > (width * 3 / 7)
                k += 1
                n = end
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
    # 灰度处理
    gray_image = cv.cvtColor(uniformed_image, cv.COLOR_RGB2GRAY)
    # 自适应阈值
    ret, binary_image = cv.threshold(gray_image, 170, 255, cv.THRESH_BINARY)  # +cv.THRESH_OTSU
    plate_binary_img = remove_upanddown_border(binary_image)
    cropImgs = char_segmentation(plate_binary_img)
    return cropImgs
