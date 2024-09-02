import os
import xml.etree.ElementTree as ET

os.chdir(os.path.dirname(__file__))
# 設定資料夾的相對路徑
ANNOTATIONS_DIR = os.path.join('..', 'Helmet', 'Annotations')
IMAGES_DIR = os.path.join('..', 'Helmet', 'Train')

# 類別對應表
CLASS_MAPPING = {
    'With Helmet': 0,
    'Without Helmet': 1
}

def parse_annotation(xml_file):
    """
    解析 XML 標註檔案，提取物件的邊界框及其標籤。
    :param xml_file: XML 標註檔案路徑
    :return: 圖片名稱, 標註列表 (每個標註包含類別與邊界框)
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    objects = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        class_id = CLASS_MAPPING.get(name)
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 轉換為 YOLO 格式
        x_center = (xmin + xmax) / 2 / width
        y_center = (ymin + ymax) / 2 / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height

        objects.append((class_id, x_center, y_center, box_width, box_height))

    return filename, objects

def save_yolo_format(filename, objects):
    """
    保存 YOLO 格式的標註文件。
    :param filename: 圖片檔案名稱
    :param objects: 標註列表 (每個標註包含類別與邊界框)
    """
    txt_filename = os.path.splitext(filename)[0] + '.txt'
    txt_path = os.path.join(IMAGES_DIR, txt_filename)

    with open(txt_path, 'w') as f:
        for obj in objects:
            class_id, x_center, y_center, box_width, box_height = obj
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

def main():
    """
    主函數：讀取所有 XML 標註檔案，並生成對應的 YOLO 格式標註文件。
    """
    for xml_file in os.listdir(ANNOTATIONS_DIR):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(ANNOTATIONS_DIR, xml_file)
            filename, objects = parse_annotation(xml_path)
            save_yolo_format(filename, objects)

if __name__ == '__main__':
    main()
