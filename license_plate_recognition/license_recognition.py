import numpy as np
from license_preprocessing import license_getcontours, license_locate, license_rotate, license_split
from keras.models import load_model
from flask import Flask, request, redirect, url_for, Response
from utils.qiniu_util import upload
import cv2 as cv
import numpy as np
import urllib.request
import json

app = Flask(__name__)
model_chs = None
model_eng = None
dict_chs = {
    '0': '川',
    '1': '颚',
    '2': '赣',
    '3': '甘',
    '4': '贵',
    '5': '桂',
    '6': '黑',
    '7': '沪',
    '8': '冀',
    '9': '津',
    '10': '京',
    '11': '吉',
    '12': '辽',
    '13': '鲁',
    '14': '蒙',
    '15': '闽',
    '16': '宁',
    '17': '青',
    '18': '琼',
    '19': '陕',
    '20': '苏',
    '21': '晋',
    '22': '皖',
    '23': '湘',
    '24': '新',
    '25': '豫',
    '26': '渝',
    '27': '粤',
    '28': '云',
    '29': '藏',
    '30': '浙'
}
dict_eng = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': 'A',
    '11': 'B',
    '12': 'C',
    '13': 'D',
    '14': 'E',
    '15': 'F',
    '16': 'G',
    '17': 'H',
    '18': 'J',
    '19': 'K',
    '20': 'L',
    '21': 'M',
    '22': 'N',
    '23': 'P',
    '24': 'Q',
    '25': 'R',
    '26': 'S',
    '27': 'T',
    '28': 'U',
    '29': 'V',
    '30': 'W',
    '31': 'X',
    '32': 'Y',
    '33': 'Z',
}


def my_predict_classes(predict_data):
    if predict_data.shape[-1] > 1:
        return predict_data.argmax(axis=-1)
    else:
        return (predict_data > 0.5).astype('int32')


def process(original_image):
    # 初始化设置图片文件位置
    original_image = original_image
    # 获取轮廓
    contours = license_getcontours(original_image)
    # 获取车牌
    res_contours, candidate_regions = license_locate(original_image, contours)
    # cv.imshow('img', candidate_regions[0])
    # cv.waitKey()
    # cv.destroyAllWindows()
    all_cropImgs = []
    for i in range(len(res_contours)):
        res_contour = res_contours[i]
        # 将车牌旋转
        rotate_image = license_rotate(original_image, res_contour)
        # cv.imshow('rotate_image', rotate_image)
        # cv.waitKey()
        # cv.destroyAllWindows()
        # 旋转后继续提取
        # 获取轮廓
        rotate_contours = license_getcontours(rotate_image)
        # 获取车牌
        new_contours, candidate_regions = license_locate(rotate_image, rotate_contours)
        # cv.imshow('rotate_image', candidate_regions[0])
        # cv.waitKey()
        # cv.destroyAllWindows()
        # 车牌分割
        for j in range(len(candidate_regions)):
            cropImgs = license_split(candidate_regions[j])
            # for img in cropImgs:
            #
            #     cv.imshow('img', img)
            #     cv.waitKey()
            #     cv.destroyAllWindows()
            all_cropImgs.append(cropImgs)

    return all_cropImgs, candidate_regions


@app.route("/pic")
def request_url_pic():
    global model_chs
    global model_eng
    if model_chs is None:
        model_path_chs = './model/license_model_chs.h5'
        model_chs = load_model(model_path_chs)
    if model_eng is None:
        model_path_eng = './model/license_model_eng.h5'
        model_eng = load_model(model_path_eng)

    pic_url = request.values.get("pic")

    resp = urllib.request.urlopen("http://rgbvrgbry.hb-bkt.clouddn.com/" + pic_url)

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    plate_image = cv.imdecode(image, cv.IMREAD_COLOR)

    # 处理
    all_cropImgs, candidate_regions = process(plate_image)
    all_y_preds = []
    res_indexes = []
    for k in range(len(all_cropImgs)):
        cropImgs = all_cropImgs[k]
        y_preds = []
        j = 0
        for img in cropImgs:
            # cv.imshow('img', img)
            # cv.waitKey()
            # cv.destroyAllWindows()
            if (j == 7):
                break
            # cv.imshow('img', img)
            # cv.waitKey()
            # cv.destroyAllWindows()
            img = img / 32.0

            img = np.expand_dims(img, axis=2)
            img = np.expand_dims(img, axis=0)
            if j == 0:
                y_predict = model_chs.predict(img)
                y_pre = my_predict_classes(y_predict)
                y_preds.append(dict_chs.get(str(y_pre[0])))
            else:
                y_predict = model_eng.predict(img)
                y_pre = my_predict_classes(y_predict)
                y_preds.append(dict_eng.get(str(y_pre[0])))
            j += 1
        if (len(y_preds) != 7):
            continue

        ch = ''
        license = ch.join(y_preds)
        all_y_preds.append(license)
        res_indexes.append(k)
        k += 1

    print(all_y_preds)
    if len(res_indexes) != 0:
        p = -1
        for l in res_indexes:
            p += 1
            upload(str(p) + '_' + "classify_" + pic_url, candidate_regions[l])
        response = {"classify_pic": str(p) + '_' + "classify_" + pic_url, "licenselist": all_y_preds}
    else:
        response = {"classify_pic": '', "licenselist": []}
    return Response(json.dumps(response), mimetype='application/json')


@app.route("/video")
def request_url_video():
    global model_chs
    global model_eng
    if model_chs is None:
        model_path_chs = './model/license_model_chs.h5'
        model_chs = load_model(model_path_chs)
    if model_eng is None:
        model_path_eng = './model/license_model_eng.h5'
        model_eng = load_model(model_path_eng)

    video_url = request.values.get("video")
    cap = cv.VideoCapture("http://rgbvrgbry.hb-bkt.clouddn.com/" + video_url)  # 设置视频流容器
    count = 0
    p = -1
    all_y_preds = []
    while count < 120:
        success, frame = cap.read()  # 读取视频流（successs代表读取成功，为True；frame为读取图片）
        if success:
            if count % 12 == 1:  # 每12帧取一次图片
                # 处理
                all_cropImgs, candidate_regions = process(frame)
                res_indexes = []
                for k in range(len(all_cropImgs)):
                    cropImgs = all_cropImgs[k]
                    y_preds = []
                    j = 0
                    for img in cropImgs:
                        # cv.imshow('img', img)
                        # cv.waitKey()
                        # cv.destroyAllWindows()
                        if (j == 7):
                            break
                        # cv.imshow('img', img)
                        # cv.waitKey()
                        # cv.destroyAllWindows()
                        img = img / 32.0

                        img = np.expand_dims(img, axis=2)
                        img = np.expand_dims(img, axis=0)
                        if j == 0:
                            y_predict = model_chs.predict(img)
                            y_pre = my_predict_classes(y_predict)
                            y_preds.append(dict_chs.get(str(y_pre[0])))
                        else:
                            y_predict = model_eng.predict(img)
                            y_pre = my_predict_classes(y_predict)
                            y_preds.append(dict_eng.get(str(y_pre[0])))
                        j += 1
                    if (len(y_preds) != 7):
                        continue

                    ch = ''
                    license = ch.join(y_preds)
                    all_y_preds.append(license)
                    res_indexes.append(k)
                    k += 1

                print(all_y_preds)
                if len(res_indexes) != 0:
                    for l in res_indexes:
                        p += 1
                        upload(str(p) + '_' + "classify_" + video_url, candidate_regions[l])
        count += 1
    cap.release()
    if (len(all_y_preds) == 0):
        response = {"classify_pic": '', "licenselist": []}
    else:
        response = {"classify_pic": str(p) + '_' + "classify_" + video_url, "licenselist": all_y_preds}

    return Response(json.dumps(response), mimetype='application/json')


if __name__ == '__main__':
    app.run()
