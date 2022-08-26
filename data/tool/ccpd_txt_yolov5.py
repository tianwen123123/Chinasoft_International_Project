import shutil
import cv2
import os
# 02-88_87-312&441_562&526-561&528_311&523_304&439_554&444-0_0_3_32_6_32_31-123-22.jpg
# 02 车牌区域占整个画面的比例
# 88_87 车牌水平和垂直角度，水平88度，竖直87度
# 312&441_562&526 标注框左上、右下的坐标，左上（312，441），右下（562，526）
# 561&528_311&523_304&439_554&444 标注框四个角点的坐标，顺序为右下、左下、左上、右上
# 0_0_3_32_6_32_31 车牌号码的映射，
# 第一个0为省份，省份：[“皖”, “沪”, “津”, “渝”, “冀”, “晋”, “蒙”, “辽”, “吉”, “黑”, “苏”, “浙”, “京”, “闽”, “赣”, “鲁”, “豫”, “鄂”, “湘”, “粤”, “桂”, “琼”, “川”, “贵”, “云”, “藏”, “陕”, “甘”, “青”, “宁”, “新”]
# 第二个0是是该车所在地的地市一级代码，地市：[‘A’, ‘B’, ‘C’, ‘D’, ‘E’, ‘F’, ‘G’, ‘H’, ‘J’, ‘K’, ‘L’, ‘M’, ‘N’, ‘P’, ‘Q’, ‘R’, ‘S’, ‘T’, ‘U’, ‘V’, ‘W’,‘X’, ‘Y’, ‘Z’]
# 后五位3_32_6_32_31为字母和文字，
# 车牌字典：[‘A’, ‘B’, ‘C’, ‘D’, ‘E’, ‘F’, ‘G’, ‘H’, ‘J’, ‘K’, ‘L’, ‘M’, ‘N’, ‘P’, ‘Q’, ‘R’, ‘S’, ‘T’, ‘U’, ‘V’, ‘W’, ‘X’,‘Y’, ‘Z’, ‘0’, ‘1’, ‘2’, ‘3’, ‘4’, ‘5’, ‘6’, ‘7’, ‘8’, ‘9’]
# --皖AD6F65
# txt标签文件生成函数
def txt_translate(path, txt_path):
    dimg_dir = os.listdir(path)
    for filename in dimg_dir:
        print(filename)
        # 第一次分割，以减号'-'做分割
        list1 = filename.split("-", 3)         # 02,88_87,312&441_562&526,...
        subname = list1[2]                     # 312&441_562&526 标注框左上、右下的坐标
        list2 = filename.split(".", 1)         # 文件格式检查
        subname1 = list2[1]                    # jpg
        if subname1 == 'txt':
            continue
        # 第二次分割，以下划线'_'做分割
        lt, rb = subname.split("_", 1)         # lt左上312&441, rb右下562&526
        lx, ly = lt.split("&", 1)              # 拆分坐标
        rx, ry = rb.split("&", 1)
        # bounding box的宽和高
        width = int(rx) - int(lx)
        height = int(ry) - int(ly)
        # bounding box中心点
        cx = float(lx) + width / 2
        cy = float(ly) + height / 2

        img = cv2.imread(path + filename)
        # 自动删除失效图片（下载过程有的图片会存在无法读取的情况）
        if img is None:
            os.remove(os.path.join(path, filename))
            continue
        width = width / img.shape[1]           # 车牌宽度/图像宽度--比例
        height = height / img.shape[0]         # 车牌高度/图像高度
        cx = cx / img.shape[1]                 # 中心点位置
        cy = cy / img.shape[0]

        txtname = filename.split(".", 1)
        txtfile = txt_path + txtname[0] + ".txt"

        with open(txtfile, "w") as f:
            f.write(str(cx) + " " + str(cy) + " " + str(width) + " " + str(height))


if __name__ == '__main__':
    # det图片存储地址
    trainDir = r"D:\Python\workspace\shuqi\chepai\ccpd\img\train"
    validDir = r"D:\Python\workspace\shuqi\chepai\ccpd\img\val"
    testDir = r"D:\Python\workspace\shuqi\chepai\ccpd\img\test"
    # det txt存储地址
    train_txt_path = r"D:\Python\workspace\shuqi\chepai\ccpd\labels\train"
    val_txt_path = r"D:\Python\workspace\shuqi\chepai\ccpd\labels\val"
    test_txt_path = r"D:\Python\workspace\shuqi\chepai\ccpd\labels\test"
    txt_translate(trainDir, train_txt_path)
    txt_translate(testDir, test_txt_path)
    txt_translate(validDir,val_txt_path)