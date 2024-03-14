import os
import time
import re
import json
import yaml
from datetime import datetime
from numbers import Integral

import logging

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from collections import defaultdict

from docx import Document

from PIL import Image
from PIL import Image

import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font

from Tool.Tool_Web import *
from Tool.Tool_Data import *
from Tool.Tool_SQL import *


## ! 可记录搜索结果，asin的位置，即反查排名位置

class AmazonSearch:
    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait, actions: ActionChains
    ):
        self.driver, self.wait, self.actions = driver, wait, actions
        self.static_value()
        # 生成当前时间的字符串，格式为 YYYYMMDD_HHMM
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        # 设置文档文件名为当前时间
        self.docfilename = f"brick4_output_{current_time}.docx"
        self.projectroot = os.path.dirname(os.path.abspath(__file__))
        self.docfilepath = os.path.join(
            self.projectroot, self.docfilename
        )
        self.doc = Document()

    def static_value(self):
        pass

    # 调试时，每次get_Search都运行一次
    def info_init(self):
        pass

    def append_line(self, line, flag=True):
        if flag:
            # 追加一行到文档中
            self.doc.add_paragraph(line)
            # 保存文档
            self.doc.save(self.docfilepath)
        print(line)
        
    def append_dict(self, dict):        
        # 迭代字典并添加内容
        for key, value in dict.items():
            self.doc.add_paragraph(f"{key}: {value}")
        # 保存文档
        self.doc.save(self.docfilepath)

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
        # sheet_ASIN_path =  f'{config["info_file_path"]}产品竞品\\{file_name}'
        # wb = load_workbook(sheet_ASIN_path, data_only=False)
        # sheet_ASIN = wb['Sheet1']    
        # seller_quickview_path = f'D:\\AutoRPA\\卖家精灵\\{ASIN}\\seller_quickview.png' //pic_files = get_files_by_name(pic_floder, '1500')
        # pyxl_draw(sheet_ASIN_path, wb, 'Sheet1', ASIN, pic_files, row_index, 11, min(len(pic_files), 8), 46, 8, False)  # type: ignore

    def read_excel(self, path):
        

    # 搜索栏输入关键词
    def start_search(self, search_words):
        search_box = self.driver.find_element(
            By.XPATH, '//*[@id="twotabsearchtextbox"]'
        )
        search_box.send_keys(search_words)
        self.driver.find_element(By.ID, "nav-search-submit-button").click()
        self.append_line(f'输入关键词{search_words}')

    def garb_search(self):
        pass

    # 获取div的特征值 
    def get_div_features(self, parent, level=0,flag=False):
        # 获取父元素的标签名
        tag_name = parent.tag_name
        # 获取父元素的class属性
        attributes = parent.get_attribute("class")
        # 获取父元素的父元素
        pre_parent = parent.find_element(By.XPATH, '..')
        # 获取父元素的所有同类型的同级元素
        elements = pre_parent.find_elements(By.TAG_NAME, parent.tag_name)
        i = 0
        # 递归时，当前步骤中的parent不是第一次输入的值时
        if level != 0:
            # 遍历同级元素列表
            for i, elem in enumerate(elements):
                # 当遍历到当前元素时，记录当前元素在同级元素中的位置
                if elem != parent:
                    i = i + 1
                # 当循环到自己时，停止循环，避免过度循环
                elif elem == parent:
                    break
        # 标签类型，层级，该层级下有多少个相关元素，class的值，[]下一级元素内容
        feature = [tag_name, level, i, attributes, []]
        if flag:
            space_interval = level*"  "
            self.append_line(f'{space_interval}{feature}')
        # 遍历当前div元素的子元素
        for child in parent.find_elements(By.XPATH, './*'):
            # 对每个子元素递归调用get_div_features()函数，获取子元素的特征
            child_feature = self.get_div_features(child, level + 1, flag)
            # 将子元素的特征添加到当前div元素的特征列表中
            feature[4].append(child_feature)
        return feature

    def get_element_structure(self, element, level=0):
        outer_html = element.get_attribute('outerHTML')
        soup = BeautifulSoup(outer_html, "html.parser")
        # 使用prettify()函数将HTML代码美化
        pretty_html = soup.prettify()
        # 打印美化后的HTML代码，每行打印一次
        for line in pretty_html.split('\n'):
            self.append_line(line)

    # 比对div的特征值，找到配置文件中对应的section，在section中根据数据位置获取数据
    # 如果特征值在配置文件中没有找到，则保存特征值
    def match_feature_data(self, div_Info_child, config_name):
        config_file = 'yaml/features_result_'+config_name+'.yml'
        # 获取项目根目录路径
        root_folder = os.path.dirname(os.path.abspath(__file__))
        config_img = os.path.join(root_folder, 'yaml', f'img_{config_name}')
        
        self.append_line(f'&&当前ASIN下的div元素有：{len(div_Info_child)}个')
        with open(config_file) as f:
            config = yaml.safe_load(f)
        
        # 遍历div_Info_child数组
        for index, child in enumerate(div_Info_child, 1):
            child_class = child.get_attribute("class")
            feature_symbol = None
            if child_class == '':
                feature_symbol = 'div'
            child_xpath = self.get_xpath(child)
            self.append_line(f'--当前匹配的是第 {index} 个div')
            self.append_line(f'--当前匹配的xpath：{child_xpath}')
            # 先获取div的特征值
            features_list = self.get_div_features(child, 0)
            # 将特征值转为json
            feature_str = json.dumps(features_list)
            exists = False
            self.info_all_count += 1
            key_value = None
            value = None
            # 遍历配置文件
            for section in config:
                # 匹配特征值
                if config[section]['Div_feature'] == feature_str:
                    self.count_section(section)
                    self.append_line(f'--已匹配对应的特征值section：{section}')
                    exists = True
                    key_flag = 1
                    while key_flag > 0:
                        # section中有几个需要获取的data，后缀就到几
                        key_name = f'data_{key_flag}'
                        # 匹配失败，即section的需要获取值已经到尾部，跳出循环
                        if key_name not in config[section]:
                            key_flag = -1
                            continue
                        # 匹配成功后，获取键值
                        key_value = config[section][key_name]
                        data_name = key_value[0]
                        data_method = key_value[1]
                        data_xpath = key_value[2]
                        data_type = key_value[3]
                        target_div = child.find_element(By.XPATH, data_xpath)
                        # 获取值的方式
                        # 如果data_type=hiddentext，通过js代码修改元素的class，再获取值
                        if data_method == 'xpath':
                            if data_type == 'hiddentext':
                                self.driver.execute_script(
                                    "arguments[0].className = '';", target_div
                                )
                            value = target_div.text
                        # 获取元素的属性
                        if data_method == 'attribute':
                            value = target_div.get_attribute(data_type)
                        self.append_line(f'匹配到的：{section}\t_数据名称：{data_name}\t_数据值=>{value}')
                        # 通过data_name找到self中对应名称的值，将value值赋值给self.'data_name'
                        # 如果 self 之前没有叫做 data_name 的属性，这条语句将会给 self 增加一个新的属性，并将 value 赋值给它
                        setattr(self, data_name, value)
                        key_flag = key_flag + 1
                    break  # exists = True
            new_section = None
            if not exists:
                self.get_element_structure(child)
                # 重新获取一次div特征值，并打印在文档中
                self.get_div_features(child, 0, True)
                self.info_fail_count += 1
                new_section = f'data_i.{self.data_index}_r.{self.data_cel_widget}_c.{index}'                # 当 data_index 为 None时，该div时HR下的asin
                config[new_section] = {'Div_feature': feature_str}
                self.append_line(f'!!新增元素特征值：{new_section}\t目标配置类型：{config_name}')
                with open(config_file, 'w') as f:
                    yaml.dump(config, f)
                    
                y = child.location['y']
                self.driver.execute_script(f"window.scrollTo(0, {y});")
                # 获取元素的x,y坐标
                child_x = child.location['x']
                child_y = child.location['y']
                child_width = child.size['width']
                child_height = child.size['height']
                # 截取指定区域
                self.driver.get_screenshot_as_file('screenshot.png')
                img = Image.open('screenshot.png')
                img = img.crop((child_x, 0, child_x+child_width, child_height))
                img.save(f'{config_img}\\{new_section}.png')

    # 获取基本属性信息
    def get_index(self, div):
        self.asin = div.get_attribute("data-asin")
        self.data_index = div.get_attribute("data-index")
        self.data_uuid = div.get_attribute("data-uuid")
        self.data_component_type = div.get_attribute("data-component-type")
        self.data_component_id = div.get_attribute("data-component-id")
        # value_if_true if condition else value_if_false
        self.data_cel_widget = (div.get_attribute('data-cel-widget').replace('search_result_', '') if div.get_attribute('data-cel-widget') is not None else '')
        if self.data_index == None:
            self.data_index = f'Z{div.find_element(By.XPATH, "..").get_attribute("aria-posinset")}'
        elif int(self.data_index) < 10:
            self.data_index = f'0{self.data_index}'

    # 获取div_info中的数据
    def get_search_data(self, div):
        pass

    def get_data(self, div_seller):
        pass

    def format_data(self):
        pass

    # 根据TAG_NAME及文本内容找到元素
    def get_tag_text_by_keyword(self, div, tag_name, keyword):
        spans = div.find_elements(By.TAG_NAME, tag_name)
        for span in spans:
            text = span.text
            if keyword in text:
                return text
        return None
    
    # 递归直到找到符合class_name的div
    def find_target_div_by_class(self, div, class_name):
        if div.get_attribute('class') == class_name:
            return div
        for child in div.find_elements(By.XPATH, "./div"):
            result = self.find_target_div_by_class(child, class_name)
            if result:
                return result
        return None

    # 计算section出现的次数
    def count_section(self, section_name):
        self.section_dict = defaultdict(int)
        self.section_dict[section_name] += 1

    def get_xpath(self, element):
    # 将JavaScript getXpath函数嵌入到Python代码中
        script = """
        function getElementXPath(element) {
            if (element && element.nodeType === Node.ELEMENT_NODE) {
                var xpath = '';
                var parent = null;
                for (parent = element; parent && parent !== document; parent = parent.parentNode) {
                    var index = 1;
                    for (previousSibling = parent.previousSibling; previousSibling; previousSibling = previousSibling.previousSibling) {
                        if (previousSibling.nodeName === parent.nodeName) {
                            index++;
                        }
                    }
                    xpath = '/' + parent.nodeName + '[' + index + ']' + xpath;
                }
                return xpath;
            } else {
                throw new Error('Invalid input: Element is not a valid DOM node');
            }
        }
        return getElementXPath(arguments[0]);
        """
        return self.driver.execute_script(script, element)
        # /HTML[1]/BODY[1]/DIV[3]/DIV[1]/DIV[2]/DIV[1]/DIV[2]/SPAN[1]/DIV[1]/DIV[3]


# 测试代码
if __name__ == '__main__':
    sc = ChromeStart("Seller", 9222)
    # sc.OpenPage("https://www.amazon.com/")
    sc.BindPage("https://www.amazon.com/s?k=", "Contain")
    driver, wait, actions = sc.GetDriver()
    AmazonS = AmazonSearch(driver, wait, actions)
    # AmazonS.garb_search("remote dinosaur")
    AmazonS.garb_search()

    # import cProfile
    # import pstats

    # cProfile.run("AmazonS.garb_search()", "stats.txt")
    # p = pstats.Stats('stats.txt')
    # p.strip_dirs().sort_stats(-1).self.append_line_stats()
