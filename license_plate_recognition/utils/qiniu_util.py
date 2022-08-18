from qiniu import Auth, put_file, etag
import os
from PIL import Image


path = os.curdir
path = os.path.join(path, r'temp_img')


def upload(pic_name, img):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'pyYzHH4TDtteeAPMXwCioCc5kEqL-8AxFVGadNr_'
    secret_key = 'Hje8lvBQd59-4YQus4wgA6so0WoIKYpYXeIX-xPw'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'classify-picture'
    # 上传后保存的文件名
    key = pic_name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key)

    # 将图片暂存本地
    save_local(pic_name, img)
    # 获取
    localfile = os.curdir + os.sep + pic_name
    # 要上传文件的本地路径
    ret, info = put_file(token, key, localfile)
    print(info)

    if info.status_code != 200:
        raise Exception("upload failed")

    # 删除本地缓存图
    del_local(pic_name)
    return ret, info


def save_local(pic_name, file):  # 把图片暂存到本地
    img = Image.fromarray(file)
    img.save(pic_name)


def del_local(pic_name):  # 把本地暂存的图片删除
    for maindir, a, file_name_list in os.walk(path):
        os.remove(maindir + "\\" + pic_name)


if __name__ == '__main__':
    print(path)
