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
from openpyxl.utils import column_index_from_string, get_column_letter

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
        
        self.e整合_path = os.path.join(source_root, '# 报价表整合.xlsx')
        self.e整合_wb = load_workbook(filename=self.e整合_path, read_only=False)
        self.e整合_Sheet1 = self.e整合_wb['Sheet1']
        
        self.e记录_path = os.path.join(source_root, '报价表记录.xlsx')
        self.e记录_wb = load_workbook(filename=self.e记录_path, read_only=False)
        self.e记录_Sheet1 = self.e记录_wb['Sheet1']
        self.e记录_colstr_报价表名称 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='报价表名称')
        self.e记录_colstr_品牌 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='品牌')
        self.e记录_colstr_类别 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='类别')
        self.e记录_colstr_列名行号1 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='列名行号1')
        self.e记录_colstr_列名行号2 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='列名行号2')
        self.e记录_colstr_起始位置 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='起始位置')
        self.e记录_colstr_记录时间 = self.find_colname_letter(sheet=self.e记录_Sheet1, rowindex=1, colname='记录时间')
        
        self.e对照_path = os.path.join(source_root, '报价表对照.xlsx')
        self.e对照_wb = load_workbook(filename=self.e对照_path, read_only=True)
        self.e对照_Sheet1 = self.e对照_wb['Sheet1']
        self.e对照_colstr_报价表整合列名 = self.find_colname_letter(sheet=self.e对照_Sheet1, rowindex=1, colname='报价表整合列名')
        self.e对照_colstr_是否匹配 = self.find_colname_letter(sheet=self.e对照_Sheet1, rowindex=1, colname='是否匹配')
        self.e对照_colstr_A精准匹配 = self.find_colname_letter(sheet=self.e对照_Sheet1, rowindex=1, colname='A精准匹配')
        self.e对照_colstr_A模糊匹配 = self.find_colname_letter(sheet=self.e对照_Sheet1, rowindex=1, colname='A模糊匹配')
        self.e对照_colstr_B精准匹配 = self.find_colname_letter(sheet=self.e对照_Sheet1, rowindex=1, colname='B精准匹配')
        self.e对照_colstr_B模糊匹配 = self.find_colname_letter(sheet=self.e对照_Sheet1, rowindex=1, colname='B模糊匹配')
        
        self.e目标报价表_path = None
        self.e目标报价表_wb = None

    # !计算表格的总行数和总列数
    def tool_count(self,sheet):
        row_count = 0
        while sheet.cell(row=row_count+1, column=1).value is not None:
            row_count += 1
        column_count = 0
        while sheet.cell(row=1, column=column_count+1).value is not None:
            column_count += 1       
        return row_count, column_count

    # !目标报价表：找到图片的位置和导出图片
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

    # !报价表对照：格式化报价表对照的JSON数组
    def stand_execel_contrast(self):
        e对照_wb_write = load_workbook(filename=self.e对照_path, read_only=False)
        e对照_sheet1 = e对照_wb_write['Sheet1']
        for row in e对照_sheet1.iter_rows(min_row=2, max_col=6):
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
        e对照_wb_write.save(self.e对照_path)

    # !报价表对照：读取值
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

    # !目标报价表：找到目标报价表的单元格的值
    # 1.遍历指定行（col_rowindex）的所有列，寻找名称和colname匹配的列。匹配的方式取决于在match_mode中指定的模式
    # 2.在指定的行中找不到任何匹配列，函数将返回一个错误信息。
    # 3.如果找到了匹配的列，则返回位于value_rowindex行、匹配列中的单元格的值。
    def find_colname_rowindex_value(self, sheet, rowindex, colname, value_rowindex, match_mode='精准匹配'):        
        col_index = None
        for i in range(1, sheet.max_column + 1):
            cell_value = str(sheet.cell(row=rowindex, column=i).value)
            if cell_value is None:
                break
            elif (match_mode == '精准匹配' and cell_value == colname) or \
                (match_mode == '模糊匹配' and colname in cell_value):
                col_index = i
                break
        
        if col_index is None:
            return None
        
        return sheet.cell(row=value_rowindex, column=col_index).value

    # !找到列名对应的列序号，返回字母
    def find_colname_letter(self, sheet, rowindex, colname, match_mode='精准匹配'):
        # next：这个函数会返回一个迭代器的下一个元素。
        # next 用于获取满足条件（该行的值等于colname）的第一个元素的列字母。如果没有元素满足条件，它将返回一个默认值，这里是None
        return next(
            (
                cell.column_letter
                for cell in sheet[rowindex]
                if  (match_mode == '精准匹配' and cell.value == colname) or \
                    (match_mode == '模糊匹配' and colname in cell.value)
            ),
            None,)

    # !遍历目标文件夹下对应后缀的文件
    def list_files_by_type(self, directory , file_type='.xlsx'):
        # sourcery skip: for-append-to-extend
        excel_files = []
        # 对指定目录及其所有子目录进行遍历
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(file_type):
                    excel_files.append(os.path.join(root, file))
        return excel_files

    # !报价表记录：记录报价表文件夹下所有.xlsx文件的位置信息
    def recode_excel(self):
        file_list = self.list_files_by_type(self.offer_root, '.xlsx')

        for file_path in file_list:
            ase_name = os.path.basename(file_path)
            dir_name = os.path.basename(os.path.dirname(file_path))
            pdir_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
            # any：这个函数测试可迭代的元素是否有至少一个为真。
            # any用于检查表格中是否有至少一个单元格的值等于ase_name。如果有任何一个单元格的值等于 ase_name, 则 any 函数返回 True，否则返回 False。
            ase_name_exist = any(
                cell.value == ase_name
                for cell in self.e记录_Sheet1[self.e记录_colstr_报价表名称]
            )
            if not ase_name_exist:
                报价表记录_Sheet1_maxrow, 报价表记录_Sheet1_maxcol = self.tool_count(self.报价表记录_Sheet1)
                self.e记录_Sheet1[f'{self.e记录_colstr_报价表名称}{报价表记录_Sheet1_maxrow+1}'] = ase_name
                self.e记录_Sheet1[f'{self.e记录_colstr_品牌}{报价表记录_Sheet1_maxrow+1}'] = dir_name
                self.e记录_Sheet1[f'{self.e记录_colstr_类别}{报价表记录_Sheet1_maxrow+1}'] = pdir_name
                
        self.e记录_wb.save(self.e记录_path)

    def contrast_data_fill(self):
        # sourcery skip: hoist-statement-from-loop, lift-duplicated-conditional, low-code-quality, merge-duplicate-blocks, merge-repeated-ifs, remove-redundant-if, simplify-boolean-comparison
        # 打开报价表记录
        报价表记录_Sheet1_maxrow, 报价表记录_Sheet1_maxcol = self.tool_count(self.报价表记录_Sheet1)
        print(报价表记录_Sheet1_maxrow, 报价表记录_Sheet1_maxcol)
        for i in range(2, 报价表记录_Sheet1_maxrow + 1):
            if self.e记录_Sheet1[f'{self.e记录_colstr_记录时间}{i}'].value is None:
                报价表名称 = self.e记录_Sheet1[f'{self.e记录_colstr_报价表名称}{i}'].value
                品牌 = self.e记录_Sheet1[f'{self.e记录_colstr_品牌}{i}'].value
                类别 = self.e记录_Sheet1[f'{self.e记录_colstr_类别}{i}'].value
                列名行号1 = self.e对照_Sheet1[f'{self.e记录_colstr_列名行号1}{i}'].value
                列名行号2 = self.e对照_Sheet1[f'{self.e记录_colstr_列名行号1}{i}'].value
                起始位置 = self.e对照_Sheet1[f'{self.e记录_colstr_起始位置}{i}'].value
                报价表路径 = os.path.join(self.offer_root, 类别, 品牌, 报价表名称)
                wb = load_workbook(filename=报价表路径, read_only=False)
                # 遍历目标报价表的sheet
                for sheetname in wb.sheetnames:
                    ws = wb[sheetname]
                    ws_maxrow, ws_maxcol = self.tool_count(ws)
                    # sheet的每一列
                    for i, col in enumerate(ws.iter_cols(min_row=列名行号1, max_row=ws_maxrow ,max_col=ws_maxcol), start=1):
                        col_letter = get_column_letter(i)
                        ws_列名1 = col[列名行号1]
                        ws_列名2 = col[列名行号2]
                        is_same = False
                        A_find_flag = False
                        B_find_flag = False
                        报价表整合列名 = None
                        if ws_列名1 == ws_列名2:
                            is_same = True
                        # 找到列对应报价表整合中的列名
                        for 报价表对照_row in self.e对照_Sheet1.iter_rows(min_row=2, max_col=7):
                            报价表整合列名 = 报价表对照_row[column_index_from_string(self.e对照_colstr_报价表整合列名)].value
                            是否匹配 = 报价表对照_row[column_index_from_string(self.e对照_colstr_是否匹配)].value
                            if 是否匹配 == '1':
                                continue
                            A精准匹配 = json.loads(报价表对照_row[column_index_from_string(self.e对照_colstr_A精准匹配)].value)
                            A模糊匹配 = json.loads(报价表对照_row[column_index_from_string(self.e对照_colstr_A模糊匹配)].value)
                            B精准匹配 = json.loads(报价表对照_row[column_index_from_string(self.e对照_colstr_B精准匹配)].value)
                            B模糊匹配 = json.loads(报价表对照_row[column_index_from_string(self.e对照_colstr_B模糊匹配)].value)
                            if ws_列名1 is not None and ws_列名2 is not None and is_same == True:
                                if A_find_flag == False:
                                    for exact in A精准匹配:
                                        if exact == ws_列名1:
                                            find_flag = True
                                            break
                                if A_find_flag == False:
                                    for exact in A模糊匹配:
                                        if exact in ws_列名1:
                                            find_flag = True
                                            break
                            elif ws_列名1 is not None and ws_列名2 is not None and is_same == False:
                                if A_find_flag == False:
                                    for exact in A精准匹配:
                                        if exact == ws_列名1:
                                            find_flag = True
                                            break
                                if A_find_flag == False:
                                    for exact in A模糊匹配:
                                        if exact in ws_列名1:
                                            find_flag = True
                                            break
                                if B_find_flag == False:
                                    for exact in B精准匹配:
                                        if exact == ws_列名1:
                                            find_flag = True
                                            break
                                if B_find_flag == False:
                                    for exact in B模糊匹配:
                                        if exact in ws_列名1:
                                            find_flag = True
                                            break
                            elif ws_列名1 is not None and ws_列名2 is None:
                                if A_find_flag == False:
                                    for exact in A精准匹配:
                                        if exact == ws_列名1:
                                            find_flag = True
                                            break
                                if A_find_flag == False:
                                    for exact in A模糊匹配:
                                        if exact in ws_列名1:
                                            find_flag = True
                                            break
                        # 写入报价表整合
                        报价表整合_Sheet1_目标列 = self.find_colname_letter(sheet=self.e整合_Sheet1, rowindex=1, colname=报价表整合列名)
                        报价表整合_Sheet1_maxrow, 报价表整合_Sheet1_maxcol = self.tool_count(self.e整合_Sheet1)
                        # col 是数组 0指第一行 起始位置是行号要减一
                        position = 1
                        for col_index in range(int(起始位置-1), len(col)):
                            self.e整合_Sheet1.cell(row=报价表整合_Sheet1_maxrow + position, col=报价表整合_Sheet1_目标列, value=col[col_index].value)
                            position = position +1
                        
                        self.e整合_Sheet1[f'{报价表整合_Sheet1_目标列}{报价表整合_Sheet1_maxrow}':f'{报价表整合_Sheet1_目标列}{报价表整合_Sheet1_maxrow+len(col)-int(起始位置)}']\
                            = ws[f'{col_letter}{int(起始位置)}':f'{col_letter}{len(col)}']


        self.e记录_Sheet1[f'{self.e记录_colstr_记录时间}{报价表记录_Sheet1_maxrow+1}'] = datetime.now().strftime("%Y/%m/%d %H:%M")
        # 读取报价表对照
        




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
    ex.contrast_data_fill()