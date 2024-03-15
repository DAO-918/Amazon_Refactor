
# https://blog.csdn.net/weixin_52710755/article/details/136543199
import os
import numpy as np
from PIL import Image
from openpyxl import load_workbook


# 加载 Excel 文件
workbook = load_workbook(filename=r'读取所指定的excel')
output_folder = r'导出的文件夹所在位置'
# 选择要处理的工作表
worksheet = workbook['Sheet2']

# 获取工作表中的所有图像
images = worksheet._images
image_positions = {}
# 遍历图像并打印位置信息
for index, image in enumerate(images):
    # 获取图像的左上角和右下角坐标
    row = image.anchor.to.row
    column = image.anchor.to.col
    print(f"Image position: row: {row}, column: {column}")
    pic_name = f"pic{index}.png"  # 假设图片格式为PNG
    image_positions[pic_name] = (row, column)
    data = image.ref
    with open(os.path.join(output_folder, pic_name), 'wb') as img_file:
        img_pil = Image.open(image.ref).convert("RGB")
        img_array = np.array(img_pil)
        # 将 NumPy 数组保存为图像文件
        img_pil.save(os.path.join(output_folder, pic_name))
        # 记录图片位置信息（这里假设仍需要记录）
        image_positions[pic_name] = (row, column)
        print(f"Image position: {row}, {column}, saved as '{pic_name}'")
print(image_positions)