專案簡介
本專案旨在開發一個基於YOLOv5的工地安全帽偵測系統，透過深度學習模型自動識別工地現場人員是否佩戴安全帽。
功能特點
圖像前處理：將標註文件轉換為YOLO格式，進行數據增強與清理。
模型訓練：基於自定義數據集訓練YOLOv5模型。
推論與結果生成：使用訓練好的模型對新圖像進行偵測，並將結果輸出至指定資料夾。
圖形用戶界面（GUI）：提供簡單直觀的用戶界面，用戶可以選擇檔案並查看偵測結果。
系統需求
Python 3.8+
Anaconda 4.10+
PyTorch 1.7+
Tkinter (Python GUI Library)

資料前處理： 將標註的XML文件轉換為YOLO格式，執行 src/data_preprocessing.py。
模型訓練： 執行 src/train_model.py，系統會自動根據預設配置進行模型訓練並保存最佳模型。
推論與結果生成： 使用 src/inference.py 對新圖像進行偵測，偵測結果將保存於 Helmet/Result 資料夾。
運行GUI： 執行 src/helmet_detection_gui.py 以啟動圖形用戶界面，進行文件選擇與結果檢視。

訓練資料來源:https://www.kaggle.com/datasets/andrewmvd/helmet-detection
