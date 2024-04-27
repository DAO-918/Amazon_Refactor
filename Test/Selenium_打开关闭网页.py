from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

options = webdriver.ChromeOptions()
options.binary_location = r'D:\Code\chrome-win\chrome.exe'
options.debugger_address = '127.0.0.1:9222'
options.browser_version = '114.0.5734.0'
service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')

# 定义程序路径和参数
program_path = "D:\\Code\\chrome-win\\chrome.exe"
program_args = [
    "--remote-debugging-port=9222",
    "--user-data-dir=E:\\Code\\selenium\\AutomationProfile 114 Seller 9222",
]
shortcut_path = "D:\\Code\\chrome - New Selenium 2.lnk"

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)

driver.switch_to.window(driver.window_handles[-1])
driver.execute_script("window.open()") 
driver.switch_to.window(driver.window_handles[-1])
driver.get("https://www.baidu.com")
driver.close()

driver.switch_to.window(driver.window_handles[-1])
driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[-1])
driver.get("https://www.baidu.com")
driver.close()