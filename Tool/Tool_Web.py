import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

import subprocess
from multiprocessing import Process

from PIL import Image
from PIL import Image

class ChromeSetup:
    Seller_9222 = ["Seller",9222]
    Origin_9223 = ["Origin",9223]

class ChromeStart:
    def __init__(self,extend_model="Seller",port=9222):
        self.is_bind = False
        self.extend_model=extend_model
        # 定义程序路径和参数
        self.program_path = "D:\Code\chrome-win\chrome.exe"
        if self.extend_model == 'Seller':
            self.program_args = [
                f"--remote-debugging-port={port}",
                "--user-data-dir=E:\Code\selenium\AutomationProfile 114 Seller {port}",
            ]
        elif self.extend_model == 'Origin':
            self.program_args = [
                f"--remote-debugging-port={port}",
                "--user-data-dir=E:\Code\selenium\AutomationProfile 114 Origin {port}",
            ]
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = self.program_path
        self.options.debugger_address = f'127.0.0.1:{port}'
        self.options.browser_version = '114.0.5734.0'
        self.service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
        self.driver,self.wait,self.actions = self.BindChrome()
    
    def OpenChrome(self):
        # 成功运行后，会一直挂起，不会返回。timeout=2 两秒后关闭程序并返回
        #result = subprocess.run([self.program_path] + self.program_args,check=True,timeout=2)
        result = subprocess.Popen([self.program_path] + self.program_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(5) 
        #subprocess.run的返回结果包含一个returncode属性,表示进程退出码,0表示成功执行,非0通常表示失败
        return result.returncode == 0
    
    def GetDriver(self):
        return [self.driver,self.wait,self.actions]
    
    def BindChrome(self):
        while self.is_bind==False:
            try:
                self.driver = webdriver.Chrome(service=self.service, options=self.options)
            except Exception as e:
                self.OpenChrome()
            else:
                self.is_bind = True
        self.wait = WebDriverWait(self.driver, 20)
        self.actions = ActionChains(self.driver)
        return [self.driver,self.wait,self.actions]

    def OpenPage(self,valurl:str):
        try:
            self.driver.execute_script("window.open()")
        except Exception as e:
            self.is_bind=False
            self.BindChrome
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(valurl)
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    
    def BindPage(self,valurl:str,match_mode:str):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if match_mode == "Exact":
                if self.driver.current_url == valurl:
                    return
            elif match_mode == "Contain": 
                if valurl in self.driver.current_url:
                    return
    
    def ClosePage(self):
        self.driver.close()


# 测试代码
if __name__ == '__main__':
    sc = ChromeStart("Seller")