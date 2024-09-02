import os
import yaml
import subprocess
import warnings

# 忽略未來警告
warnings.filterwarnings("ignore", category=FutureWarning)

# 檢查 GPU 狀態
import torch
print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"可用的 GPU 數量: {torch.cuda.device_count()}")
print(f"當前使用的 GPU: {torch.cuda.current_device()}")
print(f"GPU 名稱: {torch.cuda.get_device_name(0)}")

# 確保工作目錄是 src 目錄
os.chdir(os.path.dirname(__file__))

def load_data_config(config_path):
    """
    讀取數據配置文件。
    :param config_path: 配置文件的路徑
    :return: 數據配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        data_config = yaml.safe_load(file)
    return data_config

def train_yolo_model(data_config_path, model_save_path, epochs=50, batch_size=16, img_size=640):
    """
    使用命令行調用 YOLOv5 的訓練腳本來訓練模型。
    :param data_config_path: 數據配置文件的路徑
    :param model_save_path: 訓練好的模型保存路徑
    :param epochs: 訓練的輪數
    :param batch_size: 批次大小
    :param img_size: 輸入圖片的大小
    """
    # 訓練 YOLO 模型
    yolov5_train_script = os.path.join('..', 'yolov5', 'train.py')
    os.chdir(os.path.join('..', 'yolov5'))

    # 訓練命令
    command = (
        f"python {yolov5_train_script} --img {img_size} --batch {batch_size} --epochs {epochs} "
        f"--data {data_config_path} --weights yolov5s.pt --project {model_save_path} "
        f"--name yolov5_training --device 0 --cache"
    )

    # 執行命令並實時顯示輸出
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode('utf-8', errors='ignore').strip())
    
    rc = process.poll()
    return rc

if __name__ == "__main__":
    # 設置配置文件的相對路徑
    data_config_path = os.path.join('..', 'Helmet', 'data.yaml')  # 確保 data.yaml 文件已配置好
    model_save_path = os.path.join('..', 'Helmet', 'Model')  # 訓練好的模型保存路徑

    # 執行訓練
    train_yolo_model(data_config_path, model_save_path, epochs=50, batch_size=16, img_size=640)
