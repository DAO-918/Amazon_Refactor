import datetime
import pandas as pd
import openpyxl
from openpyxl.drawing.image import Image


def pdupdate(
    sheet_info, result: dict, file_path
):  # sourcery skip: extract-method, hoist-statement-from-if
    link = result['链接']
    try:
        # flag = sheet_array.loc[sheet_array['链接'] == 'https://www.amazon.co.uk/dp/B0BRN7HMDW'].index[0]
        flag = sheet_info.loc[sheet_info['链接'] == link].index[0]
    except Exception:
        # 不能赋值为false，否则if flag >= 0: 会判断为true
        flag = -1

    if flag >= 0:
        row_index = flag
        log_info = ''
        for key, value in result.items():
            if key not in ['链接', '更新信息', '更新时间']:
                old_info = str(sheet_info.loc[row_index, key])
                new_info = str(value)
                if old_info != new_info:
                    sheet_info.at[row_index, key] = new_info
                    log_info += f'{key}=>{old_info}更新为{new_info};'
        sheet_info.at[row_index, '更新信息'] = log_info
    else:
        row_index = sheet_info.shape[0] + 1
        for key, value in result.items():
            if key not in ['更新信息', '更新时间']:
                sheet_info.at[row_index, key] = str(value)
                # print(f'row:{row_index}_col:{key}_value:{value}')
                # print(f'sheet_info:{sheet_info}')

    sheet_info.loc[row_index, '更新时间'] = datetime.date.today().strftime('%Y/%m/%d')
    sheet_info.to_excel(file_path, index=False)


def pdformat(sheet_info):
    # 折扣列设置百分比格式,无小数点
    #ValueError: cannot convert float NaN to integer
    sheet_info['折扣'] = sheet_info['折扣'].str.replace('%', '').astype('int32')
    # 评分列设置1位小数
    sheet_info['评分'] = sheet_info['评分'].round(1)
    # 评价数和视频数量列设置整数格式
    sheet_info[['评价数', '视频数量']] = sheet_info[['评价数', '视频数量']].astype('int32')
    return sheet_info


def link_AutoComple(sheet_array, sheet_array_path):
    for index, row in sheet_array.iterrows():
        link = row['链接']
        asin = row['ASIN']
        country = row['国家']
        # 如果链接不为空
        if not pd.isna(link) and pd.isna(asin) and pd.isna(country):
            url_array = link.split('/')
            # 链接中间过长
            if url_array[3] != 'dp':
                ASIN = url_array[5][:10]
                Link = f'{url_array[0]}//{url_array[2]}/{url_array[4]}/{ASIN}'
            # 其他情况
            else:
                ASIN = url_array[4][:10]
                Link = f'{url_array[0]}//{url_array[2]}/{url_array[3]}/{ASIN}'

            # 从url提取国家代码
            Country = url_array[2].split('.')[-1]
            if Country == 'com':
                Country = 'us'
            elif Country == 'co.uk':
                Country = 'uk'

            sheet_array.at[index, '链接'] = Link
            sheet_array.at[index, 'ASIN'] = ASIN
            sheet_array.at[index, '国家'] = Country

        elif pd.isna(link) and not pd.isna(asin) and not pd.isna(country):
            if country == 'us':
                Link = f'https://www.amazon.com/dp/{asin}'
            elif country == 'uk':
                Link = f'https://www.amazon.co.uk/dp/{asin}'
            else:
                Link = f'https://www.amazon.{country}/dp/{asin}'
            # .at[] 是针对单个元素进行赋值的方法，只能更新一个单元格的值。
            # .loc[] 是针对切片进行赋值的方法，可以同时更新多个单元格的值。

            sheet_array.at[index, '链接'] = Link

    sheet_array.to_excel(sheet_array_path, index=False)


def pyxl_draw(
    path: str,
    wb,
    sheet: str,
    img_name: str,
    img_array: list,
    row_index: int,
    col_index: int,
    max: int,
    row_pt: int,
    col_ch: int,
    save: bool,
):
    sheet = wb[sheet]
    # 设置 row_index 行的行高 row_pt
    sheet.row_dimensions[row_index].height = row_pt  # type: ignore

    # 设置 col_index 至 col_index + max 列的宽度 col_ch
    for col in range(col_index, col_index + max):
        sheet.column_dimensions[chr(col + 64)].width = col_ch  # type: ignore

    # 在第 row_index 行的 (col_index, col_index + max) 列中插入图片
    for flag, col in enumerate(range(col_index, col_index + max)):
        img_path = img_array[flag]
        img = Image(img_path)
        # 1字符 = 8px
        # img.width = sheet.column_dimensions[chr(col + 64)].width * 8  # type: ignore # 设置图片宽度为列宽
        img.width = col_ch * 8  # type: ignore
        # 1磅 = 4/3px
        # img.height = sheet.row_dimensions[row_index].height * (4 / 3)  # type: ignore # 设置图片高度为行高
        img.height = row_pt * (4 / 3) # type: ignore
        # img_name = f'{img_name}_{flag}'
        # img.anchor. = f'{img_name}_{flag}' # type: ignore
        '''
        1. 当 col = 36 时,对应的Excel列字母应该是 AJ
        2. 在代码中,使用了 chr(col + 64) 来获取列字母
        3. 但当 col 大于 26 时,这种方法就不适用了
        4. 因为从列 AA 开始,需要使用两个字母表示列,chr() 函数只返回一个字母
        '''
        if col < 26:
            column = chr(col + 64) 
        else:
            column = chr(col // 26 + 64) + chr(col % 26 + 64)
        cell_index = f'{column}{row_index}'
        sheet.add_image(img, cell_index)  # type: ignore
        # 获取最后一个插入的图片并设置名称
        # last_image = drawing[-1] # type: ignore #  NameError: name 'drawing' is not defined
        # last_image = sheet.drawing[-1] # type: ignore #  AttributeError: 'Worksheet' object has no attribute 'drawing'
        # last_image.title = img_name  # 设置自定义名称，根据需要修改

    if save:
        wb.save(path)


# 测试代码
if __name__ == '__main__':
    info_file_path = 'D:\\AutoRPA\\产品信息\\'
    sheet_array_path = f'{info_file_path}ASIN_Array_抓取队列.xlsx'
    sheet_info_path = f'{info_file_path}ASIN_Array_信息汇总.xlsx'
    sheet_array = pd.read_excel(sheet_array_path, sheet_name='Sheet1')
    sheet_info = pd.read_excel(sheet_info_path, sheet_name='Sheet1')
    # 调用方法补全链接
    # link_AutoComple(sheet_array, sheet_array_path)

    '''
    path = 'D:\\AutoRPA\\产品信息\\'
    wb_path = f'{path}ASIN_Info-.xlsx'
    wb = openpyxl.load_workbook(wb_path)
    sheet = wb['竞品分析-Part1']
    '''
    path = r'D:\AutoRPA\产品信息\ASIN_Info-.xlsx'
    # wb_path = f'{path}ASIN_Info-.xlsx'
    wb = openpyxl.load_workbook(path)
    sheet = wb['竞品分析-Part1']
    img_array = [
        r'D:\AutoRPA\产品图片\B07TFBGXKC\B07TFBGXKC_450_0.jpg',
        r'D:\AutoRPA\产品图片\B07TFBGXKC\B07TFBGXKC_450_1.jpg',
        r'D:\AutoRPA\产品图片\B07TFBGXKC\B07TFBGXKC_450_2.jpg',
        r'D:\AutoRPA\产品图片\B07TFBGXKC\B07TFBGXKC_450_3.jpg',
    ]
    pyxl_draw(path, wb, '竞品分析-Part1', 'B07TFBGXKC', img_array, 2, 9, 4, 46, 8, True)


# 命名图片
# cell = sheet[cell_index]
# img = cell.value
# img.title = f'{img_name}_{flag}'
