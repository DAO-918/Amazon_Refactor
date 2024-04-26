from cgi import print_arguments
import os
import re
import json
from datetime import datetime
from PIL import Image
from openpyxl.drawing.image import Image as Img
from openpyxl.styles import Alignment
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from docx import Document

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup

from urllib.parse import urlparse

from docx import Document

from PIL import Image
from PIL import Image

from Tool.Tool_Web import *
from Tool.Tool_Data import *
from Tool.Tool_SQL import *

class ExcelSearch:
    def __init__(self):
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
        self.e整合_colstr_图片 = self.find_colname_letter(sheet=self.e整合_Sheet1, rowindex=1, colname='图片')
        self.e整合_colstr_命名方式 = self.find_colname_letter(sheet=self.e整合_Sheet1, rowindex=1, colname='命名方式')
        self.e整合_colstr_图片路径 = self.find_colname_letter(sheet=self.e整合_Sheet1, rowindex=1, colname='图片路径')
        self.e整合_colstr_来源 = self.find_colname_letter(sheet=self.e整合_Sheet1, rowindex=1, colname='来源')
        self.e整合_colstr_品牌 = self.find_colname_letter(sheet=self.e整合_Sheet1, rowindex=1, colname='品牌')
        self.e整合_colnum_图片 = column_index_from_string(self.e整合_colstr_图片)
        self.e整合_colnum_命名方式 = column_index_from_string(self.e整合_colstr_命名方式)
        self.e整合_colnum_图片路径 = column_index_from_string(self.e整合_colstr_图片路径)
        self.e整合_colnum_品牌 = column_index_from_string(self.e整合_colstr_品牌)
        
        self.e目标报价表_path = None
        self.e目标报价表_wb = None
        
        sc = ChromeStart("Seller", 9222)
        sc.OpenPage("https://www.google.com/")
        # sc.BindPage("https://www.google.com", "Contain")
        driver, wait, actions = sc.GetDriver()
        self.driver, self.wait, self.actions = driver, wait, actions
        # 生成当前时间的字符串，格式为 YYYYMMDD_HHMM
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        # 设置文档文件名为当前时间
        self.docfilename = f"Garb_Search_Output_{current_time}.docx"
        self.projectroot = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(self.projectroot)
        self.output_root = os.path.join(parent_directory, '# OUTPUT', os.path.basename(self.projectroot))
        self.docfilepath = os.path.join(self.output_root, self.docfilename)
        self.doc = Document()

    def start_driver(timeout=5):
        for _ in range(timeout):
            try:
                driver = webdriver.Chrome(service=service, options=options)
                driver.get("https://www.baidu.com")
                driver.execute_script("window.open()")
                return driver
            except Exception:
                # 确保只有一个Chrome程序正在运行
                os.system('taskkill /f /im chrome.exe')
                start_chrome_program()
                sleep(2)
        # 返回None如果在超时时间内都无法成功启动driver
        raise Exception("Failed to start driver within timeout.")

    def google_lens(self):
        
        pass

# 测试代码
if __name__ == '__main__':
    ex = ExcelSearch()
