import os
import cv2
import random
from pathlib import Path
import tensorflow as tf
from models.config import TABLE_PATH, NUM_CLASSES,OUTPUT_SHAPE

#字典查询器
table = tf.lookup.StaticHashTable(
            tf.lookup.TextFileInitializer(
                TABLE_PATH, 
                tf.string, 
                tf.lookup.TextFileIndex.WHOLE_LINE, 
                tf.int64, tf.lookup.TextFileIndex.LINE_NUMBER
            ), 
        NUM_CLASSES-2)

#数据预处理方法
def preprocess_image(image, train = True):
    if train:
        image_shape = (32, 320, 3)
    else:
        image_shape = (32, 1280, 3)
    img = tf.image.decode_jpeg(image, channels=3)
    imgH, imgW, imgC = image_shape
    resized_image = tf.image.resize(img, [imgH, imgW],preserve_aspect_ratio=True)
    resized_image = resized_image / 255
    resized_image -= 0.5
    resized_image /= 0.5
    padding_im = tf.image.pad_to_bounding_box(resized_image,0,0,imgH, imgW)
    return padding_im

def load_and_preprocess_image(path,label):
    image = tf.io.read_file(path)
    return preprocess_image(image),label

def load_and_preprocess_image_pridict(path):
    image = tf.io.read_file(path)
    return preprocess_image(image, train = False)

def load_and_preprocess_image_draw(path):
    image = tf.io.read_file(path)
    img = tf.image.decode_jpeg(image, channels=3)
    return img

def decode_label(img,label):
    chars = tf.strings.unicode_split(label, "UTF-8")
    tokens = tf.ragged.map_flat_values(table.lookup, chars)
    tokens = tokens.to_sparse()
    return img,tokens


def get_image_path(dir_path):
    '''
    获取图片路径列表,及其标签列表
    '''
    images  = []
    train_all_image_paths = []
    train_all_image_labels = []
    val_all_image_paths = []
    val_all_image_labels = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if '.jpg' in file:
                file_path = os.path.join(root, file)
                label_path = file_path.replace('.jpg','.txt')
                if Path(file_path.replace('.jpg','.txt')).exists():
                    with open(label_path) as f:
                        label = f.read().strip()
                    imgs= cv2.imread(file_path)
                    if imgs.shape[1]/imgs.shape[0] <= 10 and len(label)>0:
                        images.append((file_path, label))
    random.shuffle(images)
    for image,label in images:
        random_num = random.randint(1,80)
        if random_num == 5:
            val_all_image_paths.append(image)
            val_all_image_labels.append(label)
        else:
            train_all_image_paths.append(image)
            train_all_image_labels.append(label)
    return train_all_image_paths, train_all_image_labels,val_all_image_paths,val_all_image_labels