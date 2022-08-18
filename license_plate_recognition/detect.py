import cv2 as cv
import numpy as np
import os
import joblib

from keras.models import load_model
import os
import pathlib
import tensorflow as tf

AUTOTUNE = tf.data.experimental.AUTOTUNE
model_path = './model/license_model.h5'
root_dir=os.getcwd() + os.sep + "datasets/test"
root_dir_path=pathlib.Path(root_dir)
all_image_filename=[str(jpg_path) for jpg_path in root_dir_path.glob('**/*.jpg')]
all_image_label=[pathlib.Path(image_file).parent.name for image_file in all_image_filename]
all_image_unique_labelname=list(set(all_image_label))
print(len(all_image_unique_labelname))
name_index = dict((name,index) for index,name in enumerate(all_image_unique_labelname))
all_image_label_code=[name_index[pathlib.Path(path).parent.name] for path in all_image_filename]

# 生成datasete
# 基于文件名、标签 生成 特征->标签
def get_image(filename,label):
    # 借助tf读入图片
    image_data=tf.io.read_file(filename)
    image_jpg=tf.image.decode_jpeg(image_data)
    image_resized=tf.image.resize(image_jpg,[32,32])
    image_scale=image_resized/32.0
    return image_scale,label

tf_test_feature_filenames=tf.constant(all_image_filename)
tf_test_labels=tf.constant(all_image_label_code)
test_dataset=tf.data.Dataset.from_tensor_slices((tf_test_feature_filenames,tf_test_labels))

test_dataset=test_dataset.map(map_func=get_image,num_parallel_calls=AUTOTUNE)

test_dataset = test_dataset.shuffle(buffer_size=200000)
test_dataset = test_dataset.batch(batch_size=32)
test_dataset = test_dataset.prefetch(AUTOTUNE)

model = load_model(model_path)
model.compile(
    loss=tf.keras.losses.sparse_categorical_crossentropy,
    metrics=["accuracy"]
)
# x_test=[]
# y_test=[]
# for i in range(len(all_image_filename)):
#     img_path=all_image_filename[i]
#     img_label=all_image_label[i]
#     pic,label=get_image(img_path,img_label)
#     x_test.append(pic)
#     y_test.append(label)
loss,accuracy=model.evaluate(test_dataset)
print("loss:",loss,",accuracy:",accuracy)

