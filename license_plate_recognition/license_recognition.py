import numpy as np
from load_datasets import load_datasets_license
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
    '1': '赣',
    '2': '甘',
    '3': '贵',
    '4': '桂',
    '5': '黑',
    '6': '沪',
    '7': '冀',
    '8': '津',
    '9': '京',
    '10': '吉',
    '11': '辽',
    '12': '鲁',
    '13': '蒙',
    '14': '闽',
    '15': '宁',
    '16': '青',
    '17': '琼',
    '18': '陕',
    '19': '苏',
    '20': '晋',
    '21': '皖',
    '22': '湘',
    '23': '新',
    '24': '豫',
    '25': '渝',
    '26': '粤',
    '27': '云',
    '28': '藏',
    '29': '浙'
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
    # 将车牌旋转
    rotate_image = license_rotate(original_image, res_contours)
    # 旋转后继续提取

    # 获取轮廓
    contours = license_getcontours(rotate_image)
    # 获取车牌
    res_contours, candidate_regions = license_locate(rotate_image, contours)
    # cv.imshow('candidate_regions', candidate_regions[0])
    # cv.waitKey()
    # cv.destroyAllWindows()
    # 车牌分割
    cropImgs = license_split(candidate_regions[0])
    # for crop in cropImgs:
    #     cv.imshow('candidate_regions', crop)
    #
    #     cv.waitKey()
    #     cv.destroyAllWindows()

    return cropImgs,candidate_regions


@app.route("/")
def request_url():
    global model_chs
    global model_eng
    if model_chs is None:
        model_path_chs = './model/license_model_chs1.h5'
        model_chs = load_model(model_path_chs)
    if model_eng is None:
        model_path_eng = './model/license_model_eng1.h5'
        model_eng = load_model(model_path_eng)

    pic_url = request.values.get("pic")
    print(pic_url)

    resp = urllib.request.urlopen("http://rgbvrgbry.hb-bkt.clouddn.com/" + pic_url)

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    plate_image = cv.imdecode(image, cv.IMREAD_COLOR)

    # 处理
    cropImgs,candidate_regions = process(plate_image)
    y_preds = []
    i=0
    for img in cropImgs:
        # cv.imshow('img', img)
        # cv.waitKey()
        # cv.destroyAllWindows()
        img = img / 32.0
        print(img.shape)

        img = np.expand_dims(img, axis=2)
        img = np.expand_dims(img, axis=0)
        if i==0:
            y_predict = model_chs.predict(img)
            y_pre = my_predict_classes(y_predict)
            print(y_pre)
            y_preds.append(dict_chs.get(str(y_pre[0])))
        else:
            y_predict = model_eng.predict(img)
            y_pre = my_predict_classes(y_predict)
            print(y_pre)
            y_preds.append(dict_eng.get(str(y_pre[0])))
        i+=1

    ch=''
    license=ch.join(y_preds)
    print(license)
    upload("classify_"+pic_url,candidate_regions[0])
    response = {"classify_pic": "classify_" + pic_url,"license":license}
    return Response(json.dumps(response), mimetype='application/json')


if __name__ == '__main__':
    app.run()
