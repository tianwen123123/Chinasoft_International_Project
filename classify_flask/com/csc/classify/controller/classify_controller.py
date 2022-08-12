from flask import Flask, request, redirect, url_for, Response
from com.csc.classify.utils import qiniu_util
import cv2 as cv
import numpy as np
import urllib.request

import json

app = Flask(__name__)


@app.route("/")
def request_url():
    pic_url = request.values.get("pic")
    print(pic_url)

    resp = urllib.request.urlopen("http://rgbvrgbry.hb-bkt.clouddn.com/" + pic_url)

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    plate_image = cv.imdecode(image, cv.IMREAD_COLOR)

    # plate_file_path = pic_url
    # plate_image = cv.imread(plate_file_path)

    # 1.图片预处理
    # 高斯模糊
    blured_image = cv.GaussianBlur(plate_image, (5, 5), 0)

    # 转成灰度图
    gray_image = cv.cvtColor(blured_image, cv.COLOR_BGR2GRAY)

    # 使用Sobel算子，求水平方向一阶导数
    # 使用cv.CV_16S
    grad_x = cv.Sobel(gray_image, cv.CV_16S, 1, 0, ksize=3)
    # 转成CV-8U-借助cv.convertScaleAbs方法
    abs_grad_x = cv.convertScaleAbs(grad_x)
    # 叠加水平和垂直（此处不用）方向，获取sobel的输出
    gray_image = cv.addWeighted(abs_grad_x, 1, 0, 0, 0)
    # 二值化操作
    is_success, threshold_image = cv.threshold(gray_image, 0, 255, cv.THRESH_OTSU)
    # 执行闭操作=>车牌连成矩形区域
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 3))
    morphology_image = cv.morphologyEx(threshold_image, cv.MORPH_CLOSE, kernel)

    contours, _ = cv.findContours(morphology_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  # 有各种参数--可查阅了解

    cv.drawContours(plate_image, contours, -1, (0, 0, 255))

    # 获取第0个轮廓
    contour = contours[0]
    rect = cv.minAreaRect(contour)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    for i in np.arange(len(box)):
        cv.circle(plate_image, tuple(box[i]), 5, (0, 0, 255), 3)

    x, y, w, h = cv.boundingRect(contour)
    cv.rectangle(plate_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 倾斜校正

    # 获取倾斜的轮廓
    contour = contours[0]
    # 获取矩形特征描述的等值线区域，返回：中心点坐标、长和宽、旋转角度
    rect = cv.minAreaRect(contour)
    # 获取整数形式的长、宽
    rect_width, rect_height = np.int0(rect[1])
    angle = np.abs(rect[2])
    if rect_width < rect_height:
        temp = rect_width
        rect_width = rect_height
        rect_height = temp
        angle = 90 + angle  # 需要理解&修改

    # boundingRect用于获取与等值线框（轮廓框）contour的四个角点正交的矩形
    x, y, w, h = cv.boundingRect(contour)
    bounding_image = plate_image[y:y + h, x:x + w]

    enlarged_width = w * 3 // 2
    enlarged_height = h * 3 // 2
    enlarged_image = np.zeros((enlarged_height, enlarged_width, plate_image.shape[2]),
                              dtype=plate_image.dtype)  # 注意参数位置，高，宽！

    x_in_larged = (enlarged_width - w) // 2
    y_in_larged = (enlarged_height - h) // 2  # ---h?w?

    # 感兴趣的区域
    roi_image = enlarged_image[y_in_larged:y_in_larged + h, x_in_larged:x_in_larged + w, :]
    cv.addWeighted(roi_image, 0, bounding_image, 1, 0, roi_image)

    # 开始旋转
    new_center = (enlarged_width // 2, enlarged_height // 2)
    # 旋转
    transform_matrix = cv.getRotationMatrix2D(new_center, 180 + angle, 1.0)
    transform_image = cv.warpAffine(enlarged_image, transform_matrix, (enlarged_width, enlarged_height))

    # 获取输出图
    output_image = cv.getRectSubPix(transform_image, (rect_width, rect_height), new_center)
    qiniu_util.upload("classify_" + pic_url, output_image)

    response = {"classify_pic": "classify_" + pic_url}
    return Response(json.dumps(response), mimetype='application/json')


if __name__ == '__main__':
    app.run()
