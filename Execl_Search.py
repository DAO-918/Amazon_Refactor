from cgi import print_arguments
import os
import re
import json
from time import sleep
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
        
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = r'D:\Code\chrome-win\chrome.exe'
        self.options.debugger_address = '127.0.0.1:9222'
        self.options.browser_version = '114.0.5734.0'
        self.service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
        
        # 定义程序路径和参数
        self.program_path = "D:\\Code\\chrome-win\\chrome.exe"
        self.program_args = [
            "--remote-debugging-port=9222",
            "--user-data-dir=E:\\Code\\selenium\\AutomationProfile 114 Seller 9222",
        ]
        self.shortcut_path = "D:\\Code\\chrome - New Selenium 2.lnk"
        
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

    def start_chrome_program(self):
        os.startfile(self.shortcut_path)
        sleep(10)
        return True

    def open_driver(self, valurl):
        # 打开valurl网页
        for i in range(1,5):
            new_driver = None
            try:
                print((f'driver.get({valurl})'))
                self.driver.get(valurl)
                break
            except Exception as e: 
                print(e)
                print(f'Exception occurred while getting page {valurl}, retrying {i+1} time')
                # 关闭可能打开的Chrome程序
                os.system('taskkill /f /im chrome.exe')
                # 启动新的Chrome程序
                self.start_chrome_program()
                sleep(2) # 等待2秒以确保程序启动
                new_driver = webdriver.Chrome(service=self.service, options=self.options)
                new_driver.maximize_window()
                new_driver.get("https://www.baidu.com")
                new_driver.execute_script("window.open()")
                wait = WebDriverWait(new_driver, 30)
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body'))) 
                # 如果driver启动失败，则抛出异常
                if new_driver is not None:
                    self.driver = new_driver
                else:
                    print(f"Failed to start driver within timeout: {i}.")
        # 1. 初始化WebDriverWait,设置最长等待时间为5秒:
        self.wait = WebDriverWait(self.driver, 30)
        # 2. 使用until方法设置等待条件:
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

    def google_lens(self):
        self.open_driver("https://www.google.com/")
        pass

    def aibaba_lens(self):
        pass

    def loop_img_search(self):
        pass

# 测试代码
if __name__ == '__main__':
    ex = ExcelSearch()
