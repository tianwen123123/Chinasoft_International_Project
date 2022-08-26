import random
import skimage.io
import skimage.filters
import os
from shutil import copy2

in_dir =r"D:\Python\workspace\shuqi\char\create"
out_dir = r"D:\Python\workspace\shuqi\char\create_blur"
tt_dirs = os.listdir(in_dir)
for tt_dir in tt_dirs:# test train
    tt_dir_file = os.path.join(in_dir,tt_dir)
    sh_dirs = os.listdir(tt_dir_file)
    #路径，新建文件夹
    out_tt_dir = os.path.join(out_dir,tt_dir)
    if not os.path.exists(out_tt_dir):
        os.mkdir(str(out_tt_dir))
    #省份
    for sh_dir in sh_dirs: # chuan
        # create 文件夹
        out_sh_dir = os.path.join(out_tt_dir,sh_dir)# test/chuan
        if not os.path.exists(out_sh_dir):
            os.mkdir(str(out_sh_dir))
        #省份下的图片
        sh_dir_file = os.path.join(tt_dir_file,sh_dir)
        img_dirs = os.listdir(sh_dir_file) # 0.jpg
        random.shuffle(img_dirs)  # 图像列表打乱
        img_num = len(img_dirs)
        num = 0
        for img_dir in img_dirs:
            if num<img_num*0.2:
                num += 1
                #create 模糊后的图片路径
                out_img_dir = os.path.join(out_sh_dir,img_dir)
                #图片路径
                img_dir_file = os.path.join(sh_dir_file,img_dir)
                image = skimage.io.imread(fname=img_dir_file)
                sigma = 1.0
                # 高斯模糊
                blurred = skimage.filters.gaussian(
                    image, sigma=sigma)
                skimage.io.imsave(out_img_dir, blurred)
            else:
                num +=1
                # 模糊后的图片路径
                out_img_dir = os.path.join(out_sh_dir, img_dir)
                # 图片路径
                img_dir_file = os.path.join(sh_dir_file, img_dir)
                copy2(img_dir_file,out_img_dir)
        print(sh_dir)
    print(tt_dir)
#print("finish==")
