from __future__ import print_function

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import cv2
import random
import numpy as np
import shutil
import traceback
import copy
import sys

# 数据增强
class dataAugmentation(object):
    def __init__(self, noise=True, dilate=True, erode=True):
        self.noise = noise
        self.dilate = dilate
        self.erode = erode

    # 添加噪声
    @classmethod
    def add_noise(cls, img):
        for i in range(5):  # 添加点噪声，随机5个点
            # 随机选取x轴坐标
            temp_x = np.random.randint(0, img.shape[0])
            # 随机选取y轴坐标
            temp_y = np.random.randint(0, img.shape[1])
            # 将该点颜色值更改为255--白色
            img[temp_x][temp_y] = 255
        return img

    # 腐蚀-模拟笔画断裂
    @classmethod
    def add_erode(cls, img):
        #定义结构元素，3x3矩形
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.erode(img, kernel)
        return img

    # 膨胀-模拟笔画粘连
    @classmethod
    def add_dilate(cls, img):
        # 定义结构元素，3x3矩形
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.dilate(img, kernel)
        return img

    def do(self, img_list=[]):
        aug_list = copy.deepcopy(img_list)
        for i in range(len(img_list)):
            im = img_list[i]
            if self.noise and random.random() < 0.5:
                im = self.add_noise(im)
            if self.dilate and random.random() < 0.5:
                im = self.add_dilate(im)
            elif self.erode:
                im = self.add_erode(im)
            aug_list.append(im)
        return aug_list


# 对字体图像做等比例缩放
class PreprocessResizeKeepRatio(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def do(self, cv2_img):
        max_width = self.width
        max_height = self.height

        cur_height, cur_width = cv2_img.shape[:2]

        ratio_w = float(max_width) / float(cur_width)
        ratio_h = float(max_height) / float(cur_height)
        ratio = min(ratio_w, ratio_h)

        new_size = (min(int(cur_width * ratio), max_width),
                    min(int(cur_height * ratio), max_height))

        new_size = (max(new_size[0], 1),
                    max(new_size[1], 1),)

        resized_img = cv2.resize(cv2_img, new_size)
        return resized_img


# 查找字体的最小包含矩形--确定字体位置
class FindImageBBox(object):
    def __init__(self, ):
        pass

    def do(self, img):
        height = img.shape[0]
        width = img.shape[1]
        v_sum = np.sum(img, axis=0)
        h_sum = np.sum(img, axis=1)
        left = 0
        right = width - 1
        top = 0
        low = height - 1
        # 从左往右扫描，遇到非零像素点就以此为字体的左边界
        for i in range(width):
            if v_sum[i] > 0:
                left = i
                break
        # 从右往左扫描，遇到非零像素点就以此为字体的右边界
        for i in range(width - 1, -1, -1):
            if v_sum[i] > 0:
                right = i
                break
        # 从上往下扫描，遇到非零像素点就以此为字体的上边界
        for i in range(height):
            if h_sum[i] > 0:
                top = i
                break
        # 从下往上扫描，遇到非零像素点就以此为字体的下边界
        for i in range(height - 1, -1, -1):
            if h_sum[i] > 0:
                low = i
                break
        return (left, top, right, low)


# 把字体图像放到背景图像中
class PreprocessResizeKeepRatioFillBG(object):

    def __init__(self, width, height,
                 fill_bg=False,
                 auto_avoid_fill_bg=True,
                 margin=None):
        self.width = width
        self.height = height
        self.fill_bg = fill_bg
        self.auto_avoid_fill_bg = auto_avoid_fill_bg
        self.margin = margin

    # 文字在五项中的位置是否合适
    @classmethod
    def is_need_fill_bg(cls, cv2_img, th=0.5, max_val=255):
        image_shape = cv2_img.shape
        height, width = image_shape
        if height * 3 < width:
            return True
        if width * 3 < height:
            return True
        return False

    #放入文字
    @classmethod
    def put_img_into_center(cls, img_large, img_small, ):
        # img_small中为文字，img_large为黑色背景
        width_large = img_large.shape[1] #32
        height_large = img_large.shape[0] # 40

        width_small = img_small.shape[1] #30
        height_small = img_small.shape[0] #38

        if width_large < width_small:
            raise ValueError("width_large <= width_small")
        if height_large < height_small:
            raise ValueError("height_large <= height_small")

        start_width = (width_large - width_small) / 2 #1
        start_height = (height_large - height_small) / 2 #1

        end_height = start_height + height_small #39
        end_width = start_width + width_small # 31
        img_large[int(start_height):int(end_height),int(start_width):int(end_width)] = img_small
        return img_large

    def do(self, cv2_img):
        # 确定有效字体区域，原图减去边缘长度就是字体的区域
        if self.margin is not None:
            width_minus_margin = max(2, self.width - self.margin)
            height_minus_margin = max(2, self.height - self.margin)
        else:
            width_minus_margin = self.width
            height_minus_margin = self.height

        cur_height, cur_width = cv2_img.shape[:2]
        if len(cv2_img.shape) > 2:
            pix_dim = cv2_img.shape[2]
        else:
            pix_dim = None

        # 图像尺寸问题
        preprocess_resize_keep_ratio = PreprocessResizeKeepRatio(
            width_minus_margin,
            height_minus_margin)
        resized_cv2_img = preprocess_resize_keep_ratio.do(cv2_img)
        #文字在图像中的位置
        if self.auto_avoid_fill_bg:
            need_fill_bg = self.is_need_fill_bg(cv2_img)
            if not need_fill_bg:
                self.fill_bg = False
            else:
                self.fill_bg = True

        # 视图调整
        if not self.fill_bg:
            ret_img = cv2.resize(resized_cv2_img, (width_minus_margin,
                                                   height_minus_margin))
        else:
            if pix_dim is not None:
                norm_img = np.zeros((height_minus_margin,
                                     width_minus_margin,
                                     pix_dim),
                                    np.uint8)
            else:
                norm_img = np.zeros((height_minus_margin,
                                     width_minus_margin),
                                    np.uint8)
            # 将缩放后的字体图像置于背景图像中央
            ret_img = self.put_img_into_center(norm_img, resized_cv2_img)
        # 文字与图像边缘距离
        if self.margin is not None:
            if pix_dim is not None:
                norm_img = np.zeros((self.height,
                                     self.width,
                                     pix_dim),
                                    np.uint8)
            else:
                norm_img = np.zeros((self.height,
                                     self.width),
                                    np.uint8)
            ret_img = self.put_img_into_center(norm_img, ret_img)
        return ret_img


# 检查字体文件是否可用
class FontCheck(object):

    def __init__(self, lang_chars, width=32, height=32):
        self.lang_chars = lang_chars
        self.width = width
        self.height = height

    def do(self, font_path):
        width = self.width
        height = self.height
        try:
            # 尝试生成多个文字字符图像
            for i, char in enumerate(self.lang_chars):
                img = Image.new("RGB", (width, height), "black")  # 黑色背景
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(font_path, int(width * 0.9), )
                # 白色字体
                draw.text((0, 0), char, (255, 255, 255),
                          font=font)
                data = list(img.getdata())
                sum_val = 0
                for i_data in data:
                    sum_val += sum(i_data)
                if sum_val < 2:
                    return False
        except:
            print("fail to load:%s" % font_path)
            traceback.print_exc(file=sys.stdout)
            return False
        return True


# 生成字体图像
class Font2Image(object):

    def __init__(self,
                 width, height,
                 need_crop, margin):
        self.width = width
        self.height = height
        self.need_crop = need_crop
        self.margin = margin

    def do(self, font_path, char, rotate=0):
        find_image_bbox = FindImageBBox()
        # 生成黑色背景图像
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)
        #加载一个TrueType字体文件，并且创建一个字体对象
        font = ImageFont.truetype(font_path, int(self.width * 0.7), )
        # 白色字体
        draw.text((0, 0), char, (255, 255, 255),
                  font=font)
        # 对文字进行旋转
        if rotate != 0:
            img = img.rotate(rotate)
        data = list(img.getdata())
        sum_val = 0
        for i_data in data:
            sum_val += sum(i_data)
        if sum_val > 2:
            np_img = np.asarray(data, dtype='uint8')
            np_img = np_img[:, 0]
            # 裁剪图片大小
            np_img = np_img.reshape((self.height, self.width))
            # 找到能确定文字位置的最小框坐标
            cropped_box = find_image_bbox.do(np_img)
            left, upper, right, lower = cropped_box
            np_img = np_img[upper: lower + 1, left: right + 1]
            # 把字体放入到背景中去
            if not self.need_crop:
                preprocess_resize_keep_ratio_fill_bg = \
                    PreprocessResizeKeepRatioFillBG(self.width, self.height,
                                                    fill_bg=False,
                                                    margin=self.margin)
                np_img = preprocess_resize_keep_ratio_fill_bg.do(
                    np_img)
            return np_img
        else:
            print("img doesn't exist.")




if __name__ == "__main__":

    train_image_dir_name = "train"
    test_image_dir_name = "test"
    out_dir =r"D:\Python\workspace\shuqi\char"
    # 字体
    font_dir =r"D:\Python\workspace\shuqi\ziti"
    test_ratio =0.2
    width = 32
    height = 40
    # 是否自带背景图
    need_crop = False
    # 字体边缘的留白
    margin = 2
    # 旋转
    rotate = 8
    # 旋转的步长
    rotate_step = 1
    # 是否需要数据增强
    need_aug = True

    # 将dataset分为train和test两个文件夹分别存储
    train_images_dir = os.path.join(out_dir, train_image_dir_name)
    test_images_dir = os.path.join(out_dir, test_image_dir_name)

    if os.path.isdir(train_images_dir):
        shutil.rmtree(train_images_dir)
    os.makedirs(train_images_dir)

    if os.path.isdir(test_images_dir):
        shutil.rmtree(test_images_dir)
    os.makedirs(test_images_dir)


    char_list =['川', '鄂', '甘', '赣', '桂', '贵', '黑', '沪', '冀', '津', '京', '吉', '辽', '鲁', '蒙', '闽', '宁', '青', '琼', '陕', '苏', '晋', '皖', '湘', '新', '渝', '豫', '粤', '云', '藏', '浙']
    value_list = ['chuan', 'e1', 'gan', 'gan1', 'gui', 'gui1', 'hei', 'hu','ji', 'jin','jing', 'jl', 'liao', 'lu', 'meng', 'min', 'ning', 'qing', 'qiong','shan', 'su', 'sx', 'wan', 'xiang', 'xin', 'yu', 'yu1', 'yue', 'yun', 'zang', 'zhe']

    # 合并成新的映射关系表：（汉字：ID）
    # {'川': 'chuan', '鄂': 'e1', '甘': 'gan', '赣': 'gan1', '桂': 'gui', '贵': 'gui1', '黑': 'hei', '沪': 'hu', '冀': 'ji', '津': 'jin', '京': 'jing', '吉': 'jl', '辽': 'liao', '鲁': 'lu', '蒙': 'meng', '闽': 'min', '宁': 'ning', '青': 'qing', '琼': 'qiong', '陕': 'shan', '苏': 'su', '晋': 'sx', '皖': 'wan', '湘': 'xiang', '新': 'xin', '渝': 'yu', '豫': 'yu1', '粤': 'yue', '云': 'yun', '藏': 'zang', '浙': 'zhe'}
    lang_chars = dict(zip(char_list, value_list))
    font_check = FontCheck(lang_chars)

    # 旋转角度
    if rotate < 0:
        roate = - rotate

    # 所有可选择的旋转角度--生成list
    if rotate > 0 and rotate <= 45:
        all_rotate_angles = []
        for i in range(0, rotate + 1, rotate_step):
            all_rotate_angles.append(i)
        for i in range(-rotate, 0, rotate_step):
            all_rotate_angles.append(i)
        print(all_rotate_angles)


    # 对于每类字体进行小批量测试
    verified_font_paths = []
    # 读取字体
    for font_name in os.listdir(font_dir):
        path_font_file = os.path.join(font_dir, font_name)
        if font_check.do(path_font_file):
            verified_font_paths.append(path_font_file)

    # 生成字体
    font2image = Font2Image(width, height, need_crop, margin)


    for (char, value) in lang_chars.items():  # 外层循环是字
        image_list = []
        print(char, value)
        for j, verified_font_path in enumerate(verified_font_paths):  # 内层循环是字体
            if rotate == 0:
                image = font2image.do(verified_font_path, char)
                image_list.append(image)
            else:
                for k in all_rotate_angles:
                    image = font2image.do(verified_font_path, char, rotate=k)
                    image_list.append(image)
        print(j) # 当前为第几种字体


        if need_aug:
            data_aug = dataAugmentation()
            image_list = data_aug.do(image_list)

        # 8：2划分
        test_num = len(image_list) * test_ratio
        random.shuffle(image_list)  # 图像列表打乱
        count = 0
        for i in range(len(image_list)):
            img = image_list[i]

            if count < test_num:
                # 划分为test
                char_dir = os.path.join(test_images_dir,  value)
            else:
                # 划分为train
                char_dir = os.path.join(train_images_dir,  value)

            # 若无该路径则新建文件夹
            if not os.path.isdir(char_dir):
                os.makedirs(char_dir)

            path_image = os.path.join(char_dir, "%d.jpg" % count)
            cv2.imwrite(path_image, img)
            count += 1
        #print("finish==")