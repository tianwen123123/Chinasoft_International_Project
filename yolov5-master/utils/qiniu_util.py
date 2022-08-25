from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import os
from PIL import Image

path = os.curdir
path = os.path.join(path, r'temp_img')


def get_token(pic_name):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'pyYzHH4TDtteeAPMXwCioCc5kEqL-8AxFVGadNr_'
    secret_key = 'Hje8lvBQd59-4YQus4wgA6so0WoIKYpYXeIX-xPw'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'recognization-file'
    # 上传后保存的文件名
    key = pic_name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key)
    return token


def upload(pic_name, file, flag=True):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'pyYzHH4TDtteeAPMXwCioCc5kEqL-8AxFVGadNr_'
    secret_key = 'Hje8lvBQd59-4YQus4wgA6so0WoIKYpYXeIX-xPw'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'recognization-file'
    # 上传后保存的文件名
    key = pic_name

    if flag == False:
        # 设置转码参数
        fops = 'avthumb/mp4/s/640x360/vb/1.25m'
        # 转码是使用的队列名称
        pipeline = 'license_queue'
        # 可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
        saveas_key = urlsafe_base64_encode(bucket_name + ":" + key)
        fops = fops + '|saveas/' + saveas_key
        # 在上传策略中指定
        policy = {
            'persistentOps': fops,
            'persistentPipeline': pipeline
        }
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 18000, policy)
    else:
        token = q.upload_token(bucket_name, key)

    # 将文件暂存本地
    if flag:
        save_local(pic_name, file)
    # 获取
    localfile = os.curdir + os.sep + pic_name
    # 要上传文件的本地路径
    ret, info = put_file(token, key, localfile)
    print(info)

    if info.status_code != 200:
        raise Exception("upload failed")

    # 删除本地缓存
    if flag:
        del_local(localfile)
    return ret, info


def save_local(pic_name, file):  # 把图片暂存到本地
    img = Image.fromarray(file)
    img.save(pic_name)


def del_local(localfile):  # 把本地暂存的图片删除
    print(localfile)
    os.remove(localfile)


if __name__ == '__main__':
    print(path)
