import argparse
import platform
import sys
import threading
import time
from pathlib import Path

import pylab as p
import torch
import torch.backends.cudnn as cudnn
from license_preprocessing import preprocessing, license_split
from keras.models import load_model
from flask import Response, render_template
from utils.qiniu_util import upload
import cv2 as cv
import numpy as np
import urllib.request
from PIL import Image
import json
import requests
from flask import Flask, request
import os
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode
import uuid
from threading import Thread  # 创建线程的模块
import inspect
import ctypes

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
yolov5_dist = {}
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


@smart_inference_mode()
def run(
        weights=ROOT / 'weights/best_5l.pt',  # model.pt path(s)
        source=ROOT / 'data/images/plate.png',  # file/dir/URL/glob, 0 for webcam
        data=ROOT / 'data/ccpd.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.70,  # confidence threshold                               0.25
        iou_thres=0.45,  # NMS IOU threshold                                   0.45
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=True,  # show results                                       False
        save_txt=True,  # save results to *.txt                               False
        save_conf=True,  # save confidences in --save-txt labels                False
        save_crop=True,  # save cropped prediction boxes                              False
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        telephone=None
):
    global yolov5_dist
    isyolov5 = False
    yolov5_thread = None
    conf = 0
    cudnn.benchmark = True
    source = str(source)
    video_save_source = source  # 新加
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
        isyolov5 = True
        yolov5_dist[telephone] = dataset.threads[0]
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        p1s = []
        p2s = []
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f'{txt_path}.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        p1, p2 = annotator.box_label(xyxy, label, color=colors(c, True))
                        p1s.append(p1)
                        p2s.append(p2)
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.png', BGR=True)

            # Stream results
            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = "locate_" + video_save_source
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)

    if isyolov5:
        return dataset.threads[0]
    return p1s, p2s, conf, im0


def parse_opt(path, telephone=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'weights/best_5s.pt', help='model path(s)')
    parser.add_argument('--source', type=str,
                        default=ROOT / path,
                        help='file/dir/URL'
                             ''
                             '/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default=ROOT / 'data/ccpd.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='CPU', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--telephone', default=telephone)
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    p1s, p2s, conf, im0 = run(**vars(opt))
    return p1s, p2s, conf, im0


def my_predict_classes(predict_data):
    if predict_data.shape[-1] > 1:
        return predict_data.argmax(axis=-1)
    else:
        return (predict_data > 0.5).astype('int32')


"""
图片分类
"""


def process(p1s, p2s, plate_image, pic_url):
    all_y_preds = []
    index = -1
    for i in range(len(p1s)):
        # 预处理后图片
        pre_img = preprocessing(p1s, p2s, i, plate_image)
        if len(pre_img) == 0:
            continue
        # 分割的字符
        cropImgs = license_split(pre_img)
        # 小于7 不进行处理
        if (len(cropImgs) < 7):
            continue
        # 大于7进行处理
        j = 0
        y_preds = []
        for img in cropImgs:
            if (j == 7):
                break
            # 标准化
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

        ch = ''
        license = ch.join(y_preds)
        all_y_preds.append(license)
        index += 1
        upload(str(index) + '_' + "recognization_" + pic_url, pre_img)

    return all_y_preds, index


@app.route("/pic")
def pic_detect():
    global model_chs
    global model_eng
    if model_chs is None:
        model_path_chs = './models/license_model_chs.h5'
        model_chs = load_model(model_path_chs)
    if model_eng is None:
        model_path_eng = './models/license_model_eng.h5'
        model_eng = load_model(model_path_eng)

    pic_url = request.values.get("pic")
    resp = urllib.request.urlopen("http://rh5dq0hiv.hb-bkt.clouddn.com/" + pic_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    plate_image = cv.imdecode(image, cv.IMREAD_COLOR)

    pic_path = pic_url[:len(pic_url) - 4] + ".png"
    # 转为png
    cv.imwrite(pic_path,plate_image)
    plate_image=cv.imread(pic_path)
    response = None
    try:

        read_image=cv.imread(pic_path)
        opt = parse_opt(pic_path)
        p1s, p2s, conf, im0 = main(opt)
        os.remove(pic_path)


        all_y_preds, index = process(p1s, p2s, plate_image, pic_path)

        if len(all_y_preds) != 0:
            response = {"recognization_pic": str(index) + '_' + "recognization_" + pic_path, "licenselist": all_y_preds}
        else:
            response = {"recognization_pic": '', "licenselist": []}
    except Exception as e:
        print(e.args)
        if not (pic_path is None):
            os.remove(pic_path)
        response = {"recognization_pic": '', "licenselist": []}
        return Response(json.dumps(response), mimetype='application/json')
    return Response(json.dumps(response), mimetype='application/json')


"""
视频识别
"""


@app.route("/video")
def video_locate():
    global model_chs
    global model_eng
    if model_chs is None:
        model_path_chs = './models/license_model_chs.h5'
        model_chs = load_model(model_path_chs)
    if model_eng is None:
        model_path_eng = './models/license_model_eng.h5'
        model_eng = load_model(model_path_eng)

    video_url_simple = request.values.get("video")
    video_url = "http://rh5dq0hiv.hb-bkt.clouddn.com/" + video_url_simple
    video = requests.get(video_url, headers={
        "Connection": "keep-alive",
    }, stream=True)
    with open(video_url_simple, 'wb') as f:
        for chunk in video.iter_content(chunk_size=10240):
            f.write(chunk)

    opt = parse_opt("./" + video_url_simple)
    main(opt)
    files = {"files": open("./" + video_url_simple, 'rb'), "Content-Type": "application/octet-stream",
             "Content-Disposition": "form-data", "filename": "./" + video_url_simple}
    upload("locate_" + video_url_simple, files, False)

    capture = cv2.VideoCapture("./" + video_url_simple)
    i = 0
    all_y_preds = []
    index = -1
    count = -1
    while True:
        count += 1
        ret, frame = capture.read()
        if not ret:
            break
        if (count % 8 != 0):
            continue
        p1s = p2s = conf = None
        try:
            cv.imwrite( str(i) + "_" + video_url_simple[:len(video_url_simple) - 4] + ".png",frame)
            opt = parse_opt(str(i) + "_" + video_url_simple[:len(video_url_simple) - 4] + ".png")
            p1s, p2s, conf, im0 = main(opt)
            os.remove(str(i) + "_" + video_url_simple[:len(video_url_simple) - 4] + ".png")
        except Exception as e:
            print(e)
            os.remove(str(i) + "_" + video_url_simple[:len(video_url_simple) - 4] + ".png")
            response = {"locate_video": "",
                        "locate_pic": "",
                        "licenselist": []}
            return Response(json.dumps(response), mimetype='application/json')
        i += 1
        if conf < 0.75:
            continue
        else:
            for i in range(len(p1s)):
                # 预处理后图片
                pre_img = preprocessing(p1s, p2s, i, frame)
                if len(pre_img) == 0:
                    continue
                # 分割的字符
                cropImgs = license_split(pre_img)
                # 小于7 不进行处理
                if (len(cropImgs) < 7):
                    continue
                # 大于7进行处理
                j = 0
                y_preds = []
                for img in cropImgs:
                    if (j == 7):
                        break

                    # cv.imshow('img', img)
                    # cv.waitKey()
                    # cv.destroyAllWindows()
                    # 标准化
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
                index += 1
                ch = ''
                license = ch.join(y_preds)
                all_y_preds.append(license)
                upload(str(index) + '_' + video_url_simple[:len(video_url_simple) - 4] + ".png", pre_img)

    response = {"locate_video": "locate_" + video_url_simple,
                "locate_pic": str(index) + '_' + video_url_simple[:len(video_url_simple) - 4] + ".png",
                "licenselist": all_y_preds}

    return Response(json.dumps(response), mimetype='application/json')


"""
实时监测
"""

person_dist = {}
result_dist = {}
stop_flag = {}


# 自定义线程
class MyThread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
        self.setDaemon(True)
        self.start()

    def get_result(self):
        try:
            return self.result
        except Exception:
            # print(traceback.print_exc())
            return "threading result except"


def live_fun(telephone):
    global person_dist
    global result_dist
    global stop_flag
    person_dist[telephone] = threading.currentThread()
    stop_flag[telephone] = str(1)
    print("before:", person_dist)
    index = -1
    licenselist = []
    video = cv2.VideoCapture(0)
    fps = video.get(cv2.CAP_PROP_FPS)
    while True:
        flag = stop_flag.get(telephone)
        if (not (flag is None) and flag == "0"):
            break
        ret, frame = video.read()
        cv.imshow('frame', frame)
        key = cv2.waitKey(5)

        path = str(uuid.uuid1())
        cv.imwrite(path + ".png",frame)
        opt = parse_opt(path + ".png")
        p1s, p2s, conf, im0 = main(opt)
        os.remove(path + ".png")
        if conf < 0.80:
            continue
        if len(p1s) == 0:
            continue
        else:
            for i in range(len(p1s)):
                # 预处理后图片
                pre_img = preprocessing(p1s, p2s, i, frame)
                if len(pre_img) == 0:
                    continue
                index += 1
                upload(str(index) + "_" + path + ".png", pre_img)
                licenselist.append(str(index) + "_" + path + ".png")
    video.release()
    result_dist[threading.currentThread().ident] = licenselist
    print("before_result", licenselist)
    return licenselist


@app.route("/live_start")
def live_recognize_start():
    telephone = request.values.get("telephone")
    # status = request.values.get("status")
    # if status != "0":
    #     response = {"code": False}
    #     return Response(json.dumps(response), mimetype='application/json')
    # print("status:", status)
    try:
        p = MyThread(target=live_fun(telephone), args=(telephone,))
    except Exception as e:
        print(e)
        response = {"code": True}
        return Response(json.dumps(response), mimetype='application/json')
    response = {"code": True}
    return Response(json.dumps(response), mimetype='application/json')


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    print(type(thread))
    _async_raise(thread.ident, SystemExit)


@app.route("/live_stop")
def live_recognize_stop():
    telephone = request.values.get("telephone")
    global person_dist
    global stop_flag
    global result_dist
    stop_flag[telephone] = "0"
    print("after:", person_dist)
    p = person_dist.get(telephone)
    if not(p is None):
        p.join()
        licenselist = result_dist.get(p.ident)
        response = {"code": True, "licenselist": licenselist, "len": len(licenselist)}
    else:
        response = {"code": True, "licenselist": [], "len": 0}
    return Response(json.dumps(response), mimetype='application/json')


@app.route("/yolov5_camera_start")
def live_yolov5_start():
    telephone = request.values.get("telephone")
    try:
        opt = parse_opt("0", telephone)
        main(opt)
    except:
        return "success"

    return "success"


@app.route("/yolov5_camera_stop")
def live_yolov5_stop():
    global yolov5_dist
    p = yolov5_dist.get("18202275875")
    stop_thread(p)

    return "success"


if __name__ == "__main__":
    app.run()
