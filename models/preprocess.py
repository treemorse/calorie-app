import os
import shutil
import glob
import cv2

base_dir = 'data'
output_dir = 'data/obj'
os.makedirs(output_dir, exist_ok=True)

category_file = os.path.join(base_dir, 'category.txt')
category_map = {}
with open(category_file, 'r') as f:
    lines = f.readlines()
    for line in lines[1:]: 
        id_, name = line.strip().split('\t')
        category_map[int(id_)] = name

for i in range(1, 101):
    img_dir = os.path.join(base_dir, str(i))
    bb_info_path = os.path.join(img_dir, 'bb_info.txt')
    
    with open(bb_info_path, 'r') as bb_info_file:
        for line in bb_info_file.readlines()[1:]:
            parts = line.strip().split()
            img_file = parts[0] + '.jpg'
            bbox = parts[1:]

            img_path = os.path.join(img_dir, img_file)
            if os.path.exists(img_path):
                shutil.copy(img_path, output_dir)
            else:
                print(f"Image file {img_path} not found.")

            label_file = os.path.join(output_dir, os.path.splitext(img_file)[0] + '.txt')
            with open(label_file, 'w') as label_out:
                img = cv2.imread(img_path)
                if img is not None:
                    h, w, _ = img.shape
                    x1, y1, x2, y2 = map(int, bbox)
                    x_center = (x1 + x2) / 2 / w
                    y_center = (y1 + y2) / 2 / h
                    bbox_width = (x2 - x1) / w
                    bbox_height = (y2 - y1) / h
                    label_out.write(f"0 {x_center} {y_center} {bbox_width} {bbox_height}\n")
                else:
                    print(f"Failed to read image {img_path}")

img_paths = glob.glob(os.path.join(output_dir, '*.jpg'))
with open(os.path.join(base_dir, 'train.txt'), 'w') as train_file:
    for img_path in img_paths:
        train_file.write(f"{img_path}\n")

with open(os.path.join(base_dir, 'obj.names'), 'w') as names_file:
    for id_, name in category_map.items():
        names_file.write(f"{name}\n")

with open(os.path.join(base_dir, 'obj.data'), 'w') as data_file:
    data_file.write("classes = 100\n")
    data_file.write(f"train = {os.path.join(base_dir, 'train.txt')}\n")
    data_file.write(f"valid = {os.path.join(base_dir, 'train.txt')}\n")
    data_file.write(f"names = {os.path.join(base_dir, 'obj.names')}\n")
    data_file.write("backup = backup/\n")
