import json

# 图片大小
OUTPUT_SHAPE = (32,320,3)

#项目路径
WORK_PATH = '/root/python_project/crnn_by_tensorflow2.2.0/'

#测试文件目录
TEST_PATH = WORK_PATH + 'dataset/test/'

#字符映射表
TABLE_PATH = WORK_PATH + "dataset/table.txt"
JSON_PATH = WORK_PATH + "dataset/char.json"
with open(JSON_PATH, 'r') as f:
    chardic = json.load(f)
with open(TABLE_PATH, 'w') as fw:
    for char in chardic:
        fw.write(char+'\n')
        
        
#字符数
NUM_CLASSES = len(chardic) + 3


#数据集参数
BATCH_SIZE = 256
BUFFER_SIZE = 10000


#模型保存与否
is_save_model = False

#保存模型版本号
version = 1

#模型保存地址
export_path = WORK_PATH + 'output/crnn/{0}'.format(str(version))