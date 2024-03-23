from cgi import print_arguments
import os
from tempfile import tempdir
import time
import re
import json
import yaml
from datetime import datetime
import numpy as np
from PIL import Image
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string

from docx import Document

class ExcelConver:
    def __init__(self):
        #self.s_name = os.path.splitext(source_file)[0]
        #self.t_name = os.path.splitext(target_file)[0]
        #self.s_wb = load_workbook(filename=source_file,read_only=True)
        #self.t_wb = load_workbook(filename=target_file)
        
        # 获取当前目录的路径
        self.projectroot = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(self.projectroot)
        # 生成当前时间的字符串，格式为 YYYYMMDD_HHMM
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        # 设置文档文件名为当前时间
        docfilename = f"Execl_Read_Output_{current_time}.docx"
        output_root = os.path.join(parent_directory, '# OUTPUT', os.path.basename(self.projectroot))
        self.docfilepath = os.path.join(output_root, docfilename)
        self.doc = Document()
        
        source_root = os.path.join(parent_directory, '# 报价表整合')
        self.offer_root = os.path.join(source_root, '报价表')
        self.image_root = os.path.join(source_root, '图片库')
        self.报价表整合_path = os.path.join(source_root, '# 报价表整合.xlsx')
        self.报价表记录_path = os.path.join(source_root, '报价表记录.xlsx')
        self.报价表对照_path = os.path.join(source_root, '报价表对照.xlsx')
        self.报价表整合_wb = load_workbook(filename=self.报价表整合_path, read_only=False)
        self.报价表记录_wb = load_workbook(filename=self.报价表记录_path, read_only=False)
        self.报价表对照_wb = load_workbook(filename=self.报价表对照_path, read_only=True)
        
        self.目标报价表_path = None
        self.目标报价表_wb = None
        
    # 目标报价表：找到图片的位置和导出图片
    def excel_img_read(self):
        # 选择要处理的工作表
        worksheet = self.s_wb['Sheet2']

        # 获取工作表中的所有图像
        images = worksheet._images
        image_positions = {}
        # 遍历图像并打印位置信息
        for index, image in enumerate(images):
            # 获取图像的左上角和右下角坐标
            rownum = image.anchor.to.row
            colnum = image.anchor.to.col
            pic_name = f"{self.s_name}_{index}_{rownum}_{colnum}.png"  # 假设图片格式为PNG
            image_positions[pic_name] = (rownum, colnum)
            # data = image.ref
            with open(os.path.join(self.image_root, pic_name), 'wb') as img_file:
                # 打开文件路径为image.ref的图像文件。convert("RGB")被用来将图像转换为RGB格式。
                img_pil = Image.open(image.ref).convert("RGB")
                # 在这个NumPy数组中，图像被存储为一个三维数组，
                # 第一个维度代表图像的高度，第二个维度代表宽度，
                # 第三个维度代表颜色通道（在RGB图像中，有红、绿、蓝三个通道）。每个元素代表在该坐标位置的像素值。
                # img_array = np.array(img_pil)
                # 将 NumPy 数组保存为图像文件
                img_pil.save(os.path.join(self.image_root, pic_name))
                # 记录图片位置信息（这里假设仍需要记录）
                image_positions[pic_name] = (rownum, colnum)
        print(image_positions)

    # 报价表对照：格式化报价表的JSON数组
    def stand_execel_contrast(self):
        报价表对照_wb_write = load_workbook(filename=self.报价表对照_path, read_only=False)
        报价表对照_sheet1 = 报价表对照_wb_write['Sheet1']
        for row in 报价表对照_sheet1.iter_rows(min_row=2, max_col=6):
            for i, cell in enumerate(row, start=1):
                if i<= 2:
                    continue
                cell_value = cell.value
                if cell_value is None:
                    continue
                try:
                    json.loads(cell_value)
                except Exception:
                    new_value = cell_value.replace("[","").replace("]","").replace("'","").replace("\"","").replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace(" ","").split(",")
                    cell.value = json.dumps(new_value, ensure_ascii=False)  # convert list to json string with Chinese characters
        # 保存表格
        报价表对照_wb_write.save(self.报价表对照_path)

    def read_excel_contrast(self):
        ws = self.c_wb['Sheet1']
        # 使用 Worksheet.iter_rows() A1,B1,C1,A2,B2,C2
        for row in ws.iter_rows(min_row=2, max_col=6):
            报价表整合列名 = row[0].value
            是否匹配 = row[1].value
            A精准匹配 = json.loads(row[2].value)
            A模糊匹配 = json.loads(row[3].value)
            B精准匹配 = json.loads(row[4].value)
            B模糊匹配 = json.loads(row[5].value)
            print(报价表整合列名, 是否匹配, A精准匹配, A模糊匹配, B精准匹配, B模糊匹配)
            
    # 目标报价表：找到目标报价表的单元格
    # 1.遍历指定行（col_rowindex）的所有列，寻找名称和colname匹配的列。匹配的方式取决于在match_mode中指定的模式
    # 2.在指定的行中找不到任何匹配列，函数将返回一个错误信息。
    # 3.如果找到了匹配的列，则返回位于value_rowindex行、匹配列中的单元格的值。
    def read_excel_by_colname_findvalue(self, sheet_name, col_rowindex, colname, match_mode, value_rowindex):
        sheet = self.目标报价表_wb[sheet_name]  # 你可能需要将此处替换为具体的表名，如果你有多个表的话
        
        col_index = None
        for col in range(1, sheet.max_column + 1):
            cell_value = str(sheet.cell(row=col_rowindex, column=col).value)
            if cell_value is None:
                break
            elif (match_mode == '精准匹配' and cell_value == colname) or \
                (match_mode == '模糊匹配' and colname in cell_value):
                col_index = col
                break
        
        if col_index is None:
            return None
        
        return sheet.cell(row=value_rowindex, column=col_index).value

    # 遍历目标文件夹下对应后缀的文件
    def list_files_by_type(self, directory , file_type='.xlsx'):
        # sourcery skip: for-append-to-extend
        excel_files = []
        # 对指定目录及其所有子目录进行遍历
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(file_type):
                    excel_files.append(os.path.join(root, file))
        return excel_files

    def recode_excel(self):
        self.list_files_by_type(self.offer_root, '.xlsx')
        报价表记录_Sheet1 = self.报价表记录_wb['Sheet1'].columns
        #报价表记录_colnum_报价表名称 = self.报价表记录_wb['Sheet1'].columns.get_loc("报价表名称")
        


        报价表记录_colnum_报价表名称 = next(
            (
                column_index_from_string(cell.column_letter)
                for cell in 报价表记录_Sheet1[1]
                if cell.value == '报价表名称'
            ),
            None,
        )
        print(报价表记录_colnum_报价表名称)
        


# 测试代码
if __name__ == '__main__':
    source_file = r'D:\Code\报价表整合\报价表\明迪积木现货表2024.2.20.xlsx'
    target_file = r'D:\Code\报价表整合\报价表整合.xlsx'
    
    #ex = ExcelConver(source_file, target_file)
    #ex.stand_execel_contrast()
    #ex.read_excel_contrast()
    #value = ex.read_excel_by_colname_findvalue(sheet_name='展示盒', col_rowindex=1, colname='货号', match_mode='精准匹配', value_rowindex=2)
    #print(value)
    
    ex = ExcelConver()
    file_list = ex.list_files_by_type('D:\Code\# 报价表整合\报价表', '.xlsx')
    print(file_list)
    for file_path in file_list:
        base_name = os.path.basename(file_path)
        dir_name = os.path.basename(os.path.dirname(file_path))
        print(f'File name, including extension: {base_name}')
        print(f'Name of the parent directory: {dir_name}')
    
    ex.recode_excel()