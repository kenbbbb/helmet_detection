import torch
from pathlib import Path
import os
import shutil

# 確保工作目錄是 src 目錄
os.chdir(os.path.dirname(__file__))

def run_inference(model_path, source_folder, output_folder):
    # 加載訓練好的模型
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    model.conf = 0.25  # 設置信心閾值

    # 確保輸出資料夾存在
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # 遍歷 source_folder 中的每張圖片進行推論
    for img_name in os.listdir(source_folder):
        img_path = os.path.join(source_folder, img_name)
        if os.path.isfile(img_path):  # 確保這是文件而非資料夾
            results = model(img_path)
            temp_save_dir = Path(output_folder) / "temp"  # 暫存目錄
            results.save(save_dir=temp_save_dir)  # 保存結果到暫存目錄

            # 將暫存目錄中的結果移動到最終的 output_folder
            for file in os.listdir(temp_save_dir):
                shutil.move(os.path.join(temp_save_dir, file), output_folder)

            # 刪除暫存目錄
            shutil.rmtree(temp_save_dir)

if __name__ == "__main__":
    # 使用相對路徑
    model_path = os.path.join('..', 'Helmet', 'Model', 'yolov5_training', 'weights', 'best.pt')
    source_folder = os.path.join('..', 'Helmet', 'Detect')
    output_folder = os.path.join('..', 'Helmet', 'Result')

    run_inference(model_path, source_folder, output_folder)
