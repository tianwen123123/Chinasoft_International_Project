import os
import pathlib
import tensorflow as tf
from keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, \
    AveragePooling2D, MaxPooling2D
from keras.models import Model
from keras.initializers import glorot_uniform
import cv2 as cv

AUTOTUNE = tf.data.experimental.AUTOTUNE
model_path = 'model/license_model_chs.h5'

root_dir = os.getcwd() + os.sep + "datasets/chs_train"
root_dir_path = pathlib.Path(root_dir)
all_image_filename=[str(jpg_path) for jpg_path in root_dir_path.glob('**/*.jpg')]
all_image_label = [pathlib.Path(image_file).parent.name for image_file in all_image_filename]
all_image_unique_labelname = list(set(all_image_label))
all_image_unique_labelname.sort(key = all_image_label.index)
print(all_image_unique_labelname)
name_index = dict((name, index) for index, name in enumerate(all_image_unique_labelname))
all_image_label_code = [name_index[pathlib.Path(path).parent.name] for path in all_image_filename]


# 生成dataset
# 基于文件名、标签 生成 特征->标签
def get_image(filename, label):
    # 借助tf读入图片
    image_data = tf.io.read_file(filename)
    image_jpg = tf.image.decode_jpeg(image_data)
    image_resized = tf.image.resize(image_jpg, [32, 32])
    image_scale = image_resized / 32.0
    gray_image = cv.cvtColor(image_scale, cv.COLOR_BGR2GRAY)
    ret, binary_image = cv.threshold(gray_image, 0, 255, cv.THRESH_OTSU)
    return binary_image, label


tf_train_feature_filenames = tf.constant(all_image_filename)
tf_train_labels = tf.constant(all_image_label_code)
train_dataset = tf.data.Dataset.from_tensor_slices((tf_train_feature_filenames, tf_train_labels))
train_dataset = train_dataset.map(map_func=get_image, num_parallel_calls=AUTOTUNE)

# for sample in train_dataset:
#     print(sample)

num_epochs = 50
batch_size = 32
learning_rate = 1e-3

train_dataset = train_dataset.shuffle(buffer_size=200000)
train_dataset = train_dataset.batch(batch_size=batch_size)
train_dataset = train_dataset.prefetch(AUTOTUNE)


# 卷积块
def convolutional_block(X, f, filters, stage, block, s=2):
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    F1, F2, F3 = filters

    X_shortcut = X

    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(s, s), name=conv_name_base + '2a',
               kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2a')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=conv_name_base + '2b',
               kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), name=conv_name_base + '2c',
               kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2c')(X)

    X_shortcut = Conv2D(F3, (1, 1), strides=(s, s), name=conv_name_base + '1',
                        kernel_initializer=glorot_uniform(seed=0))(X_shortcut)
    X_shortcut = BatchNormalization(axis=3, name=bn_name_base + '1')(X_shortcut)

    X = Add()([X, X_shortcut])
    X = Activation('relu')(X)

    return X


# 恒等快
def identify_block(X, f, filters, stage, block):
    """
    X - 输入的tensor类型数据，维度为（m, n_H_prev, n_W_prev, n_H_prev）
    f - kernal大小
    filters - 整数列表，定义每一层卷积层过滤器的数量
    stage - 整数 定义层位置
    block - 字符串 定义层位置

    X - 恒等输出，tensor类型，维度（n_H, n_W, n_C）
    """
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    F1, F2, F3 = filters  # 定义输出特征的个数
    X_shortcut = X

    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2a',
               kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2a')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=conv_name_base + '2b',
               kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2c',
               kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2c')(X)
    # 没有激活

    X = Add()([X, X_shortcut])
    X = Activation('relu')(X)
    return X


def ResNet50(input_shape=(32, 32, 1), classes=31):
    """
    CONV2D -> BATCHNORM -> RELU -> MAXPOOL -> CONVBLOCK -> IDBLOCK*2 -> CONVBLOCK -> IDBLOCK*3
    -> CONVBLOCK -> IDBLOCK*5 -> CONVBLOCK -> IDBLOCK*2 -> AVGPOOL -> TOPLAYER

    input_shape: 据集维度
    classes： 分类数
    """
    # 定义一个placeholder
    X_input = Input(input_shape)
    # 0填充
    X = ZeroPadding2D((3, 3))(X_input)

    # stage1
    X = Conv2D(filters=64, kernel_size=(7, 7), strides=(2, 2), name='conv1', kernel_initializer=glorot_uniform(seed=0))(
        X)
    X = BatchNormalization(axis=3, name='bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(X)

    # stage2
    X = convolutional_block(X, f=3, filters=[64, 64, 256], stage=2, block='a', s=1)
    X = identify_block(X, f=3, filters=[64, 64, 256], stage=2, block='b')
    X = identify_block(X, f=3, filters=[64, 64, 256], stage=2, block='c')

    # stage3
    X = convolutional_block(X, f=3, filters=[128, 128, 512], stage=3, block="a", s=2)
    X = identify_block(X, f=3, filters=[128, 128, 512], stage=3, block="b")
    X = identify_block(X, f=3, filters=[128, 128, 512], stage=3, block="c")
    X = identify_block(X, f=3, filters=[128, 128, 512], stage=3, block="d")

    # stage4
    X = convolutional_block(X, f=3, filters=[256, 256, 1024], stage=4, block="a", s=2)
    X = identify_block(X, f=3, filters=[256, 256, 1024], stage=4, block="b")
    X = identify_block(X, f=3, filters=[256, 256, 1024], stage=4, block="c")
    X = identify_block(X, f=3, filters=[256, 256, 1024], stage=4, block="d")
    X = identify_block(X, f=3, filters=[256, 256, 1024], stage=4, block="e")
    X = identify_block(X, f=3, filters=[256, 256, 1024], stage=4, block="f")

    # stage5
    X = convolutional_block(X, f=3, filters=[512, 512, 2048], stage=5, block="a", s=2)
    X = identify_block(X, f=3, filters=[512, 512, 2048], stage=5, block="b")
    X = identify_block(X, f=3, filters=[512, 512, 2048], stage=5, block="c")

    # 均值池化
    X = AveragePooling2D(pool_size=(2, 2), padding='same')(X)

    # 输出层
    X = Flatten()(X)
    X = Dense(classes, activation="softmax", name='fc' + str(classes), kernel_initializer=glorot_uniform(seed=0))(X)

    model = Model(X_input, X)
    return model


model = ResNet50(input_shape=(32, 32, 1), classes=31)

model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=learning_rate, beta_1=0.9, beta_2=0.99, epsilon=1e-08, decay=0.0),
    loss=tf.keras.losses.sparse_categorical_crossentropy,
    metrics=["accuracy"]
)

model.fit(train_dataset, epochs=num_epochs)
# 模型保存
model.save(model_path)
