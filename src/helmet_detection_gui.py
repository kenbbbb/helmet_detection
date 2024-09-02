import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
import os
import shutil
from pathlib import Path

# 確保工作目錄是 src 目錄
os.chdir(os.path.dirname(__file__))

def select_folder(var):
    folder_selected = filedialog.askdirectory()
    var.set(folder_selected)

def run_inference_gui():
    model_path = os.path.join(model_folder.get(), 'yolov5_training', 'weights', 'best.pt')
    output_folder = result_folder.get()
    selected_images = img_list.curselection()  # 獲取選中的圖片索引
    selected_image_names = [img_list.get(i) for i in selected_images]  # 根據索引獲取圖片名稱

    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    model.conf = 0.25
    
    for img_name in selected_image_names:
        img_path = os.path.join(detect_folder.get(), img_name)
        if os.path.isfile(img_path):
            results = model(img_path)
            temp_save_dir = Path(output_folder) / "temp"
            results.save(save_dir=temp_save_dir)
            for file in os.listdir(temp_save_dir):
                destination = os.path.join(output_folder, file)
                if os.path.exists(destination):
                    os.remove(destination)  # 如果文件已經存在，刪除它
                shutil.move(os.path.join(temp_save_dir, file), output_folder)
            shutil.rmtree(temp_save_dir)
    
    messagebox.showinfo("Info", "Detection completed!")
    update_image_list()

def update_image_list():
    img_list.delete(0, tk.END)
    for img_name in os.listdir(detect_folder.get()):
        img_list.insert(tk.END, img_name)

def show_images(event):
    selected_indices = img_list.curselection()
    if selected_indices:
        for i in selected_indices:
            img_name = img_list.get(i)
            original_image_path = os.path.join(detect_folder.get(), img_name)
            result_image_path = os.path.join(result_folder.get(), img_name)

            try:
                original_image = Image.open(original_image_path)
                original_image = original_image.resize((200, 200))
                original_img_display = ImageTk.PhotoImage(original_image)
                original_label.config(image=original_img_display)
                original_label.image = original_img_display

                if os.path.exists(result_image_path):
                    result_image = Image.open(result_image_path)
                    result_image = result_image.resize((200, 200))
                    result_img_display = ImageTk.PhotoImage(result_image)
                    result_label.config(image=result_img_display)
                    result_label.image = result_img_display
                else:
                    # 如果結果圖片不存在，只顯示原始圖片，不顯示提示訊息
                    result_label.config(image='')

            except FileNotFoundError as e:
                print(f"Error: {e}")

root = tk.Tk()
root.title("Helmet Detection GUI")

# 使用相對路徑
train_folder = tk.StringVar(value=os.path.join("..", "Helmet", "Train"))
model_folder = tk.StringVar(value=os.path.join("..", "Helmet", "Model"))
detect_folder = tk.StringVar(value=os.path.join("..", "Helmet", "Detect"))
result_folder = tk.StringVar(value=os.path.join("..", "Helmet", "Result"))

tk.Label(root, text="Train Folder:").pack()
tk.Entry(root, textvariable=train_folder).pack()
tk.Button(root, text="Select Train Folder", command=lambda: select_folder(train_folder)).pack()

tk.Label(root, text="Model Folder:").pack()
tk.Entry(root, textvariable=model_folder).pack()
tk.Button(root, text="Select Model Folder", command=lambda: select_folder(model_folder)).pack()

tk.Label(root, text="Detect Folder:").pack()
tk.Entry(root, textvariable=detect_folder).pack()
tk.Button(root, text="Select Detect Folder", command=lambda: select_folder(detect_folder)).pack()

tk.Label(root, text="Result Folder:").pack()
tk.Entry(root, textvariable=result_folder).pack()
tk.Button(root, text="Select Result Folder", command=lambda: select_folder(result_folder)).pack()

tk.Button(root, text="Run Detection", command=run_inference_gui).pack()

# 創建圖片列表框，設置為多選模式
img_list = tk.Listbox(root, selectmode=tk.MULTIPLE)
img_list.pack()
img_list.bind('<<ListboxSelect>>', show_images)

original_label = tk.Label(root)
original_label.pack(side=tk.LEFT, padx=10)
result_label = tk.Label(root)
result_label.pack(side=tk.RIGHT, padx=10)

update_image_list()

root.mainloop()
