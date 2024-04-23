import datetime

import time
import pandas as pd
from Tool.Tools_Web_Selenium import picdownload
from Tool.Tools_Execl import pdupdate
from Tool.Tools_Init import startInit
from Tool.Chaojiying import  Chaojiying_Client

import re
import urllib.parse

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup

import os
import subprocess
import base64
from io import BytesIO
from PIL import Image
from time import sleep

import requests
from urllib.parse import unquote

import cv2  # pip install opencv-python
# 
import numpy as np

## ! 步骤二依次获取链接信息，存储到汇总

config = startInit()

sheet_array_path = config['info_file_path'] + 'ASIN_Array_抓取队列.xlsx'
sheet_info_path = config['info_file_path'] + 'ASIN_Array_信息汇总.xlsx'
sheet_array = pd.read_excel(sheet_array_path, sheet_name='Sheet1')
sheet_info = pd.read_excel(sheet_info_path, sheet_name='Sheet1')

chaojiying_seller = Chaojiying_Client('WhiteST', 'QSCZSE123', '958866')
captcha_code_seller = 'D:\\Code\\# OUTPUT\\Amazon_Refactor\\验证码\\卖家精灵'
captcha_code_seller_path = os.path.join(captcha_code_seller, 'temp.jpg')
chaojiying_amazon = Chaojiying_Client('WhiteST', 'QSCZSE123', '958867')
captcha_code_amazon = 'D:\\Code\\# OUTPUT\\Amazon_Refactor\\验证码\\亚马逊'
captcha_code_amazon_path = os.path.join(captcha_code_amazon, 'temp.jpg')


# !文件重命名
# rename_file(captcha_code_seller, 'temp.jpg', captcha_code+datetime.now().strftime("%Y%m%d_%H%M")+'.jpg')
def rename_file_basedir(directory, old_filename, new_filename):
    old_file = os.path.join(directory, old_filename)
    new_file = os.path.join(directory, new_filename)
    os.rename(old_file, new_file)

# !下载验证码图片
def analyze_url_and_save_image(url, save_path):
    if url.startswith('data:image'):
        base64_str = url.split('base64,')[-1]
        base64_str = unquote(base64_str)
        imgdata = base64.b64decode(base64_str)
        with open(save_path, 'wb') as file:
            file.write(imgdata)
    else:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)

# !检测captcha元素是否存在
def captcha_element_display(driver, xpath_name):
    if xpath_name == '卖家精灵':
        seller_container = None
        captcha_image = None
        captcha_displayed = None
        try:
            seller_container = driver.find_element(By.XPATH, "//div[contains(@class, 'robot-card-container') and contains(@style, 'display: block;')]")
            captcha_image = seller_container.find_element(By.XPATH, ".//img[contains(@class, 'h-100 show-hand-shape')]")
            # "可见" 并不等于 "存在"。一个元素可能在 DOM 中（存在），
            # 但是通过 CSS 属性（比如 display: none 或 visibility: hidden）被隐藏，那么它就不是 "可见"。
            captcha_displayed = captcha_image.is_displayed()
        except Exception as e:
            print(f'没有找到验证码元素: {str(e.msg)}') # type: ignore
        if seller_container is not None and captcha_image is not None and captcha_displayed:
            # 获取url
            try:
                image_url = captcha_image.get_attribute('src')
                captcha_code_seller = 'D:\\Code\\# OUTPUT\\Amazon_Refactor\\验证码\\卖家精灵'
                captcha_code_seller_path = os.path.join(captcha_code_seller, 'temp.jpg')
                # 判断url类型并下载
                #analyze_url_and_save_image(image_url, captcha_code_seller_path)
                if image_url.startswith('data:image'):
                    base64_str = image_url.split('base64,')[-1]
                    base64_str = unquote(base64_str)
                    imgdata = base64.b64decode(base64_str)
                    with open(captcha_code_seller_path, 'wb') as file:
                        file.write(imgdata)
                else:
                    response = requests.get(image_url)
                    with open(captcha_code_seller_path, 'wb') as file:
                        file.write(response.content)
                # 请求超级鹰
                chaojiying = Chaojiying_Client('WhiteST', 'QSCZSE123', '958866')	
                im = open(captcha_code_seller_path, 'rb').read()													
                result = chaojiying.PostPic(im, 1902)
                err_no = result['err_no']
                pic_str = result['pic_str']
                # 识别成功重命名验证码图片
                if err_no == 0: 
                    try:
                        new_filename = f"{pic_str}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.jpg"
                        captcha_code_seller_path_new = os.path.join(captcha_code_seller, new_filename)
                        os.rename(captcha_code_seller_path, captcha_code_seller_path_new)
                        form = seller_container.find_element(By.XPATH, ".//form[@name='form_signin' and @method='post']")
                        input = form.find_element(By.XPATH, ".//input[@type='text' and contains(@class, 'text-uppercase')]")
                        button = form.find_element(By.XPATH, ".//button[@type='submit' and @class='btn-ext btn-ext-primary' and text()='我不是机器人']")
                        # text不是一个方法，而是一个属性，去掉后面的括号()。
                        print(button.text)
                        if button.text != '我不是机器人':
                            print("ERROR 获取button错误")
                        actions = ActionChains(driver)
                        actions.move_to_element(input)
                        actions.perform()
                        input.send_keys(pic_str)
                        actions.move_to_element(button)
                        actions.click(button)
                        actions.perform()
                        sleep(2)
                        seller_div = driver.find_element(By.XPATH, "//div[@id='seller-sprite-extension-app']")
                        seller_footer = seller_div.find_element(By.XPATH, ".//div[contains(@class, 'ext-main-container')]")
                        seller_footer_header = seller_footer.find_element(By.XPATH, ".//header[contains(@class, 'navbar-ext')]")
                        seller_right_bar = seller_footer_header.find_element(By.XPATH, ".//div[contains(@class, 'right-form-close')]")
                        seller_right_close = seller_right_bar.find_element(By.XPATH, ".//div[contains(@class, 'sign-in-close')]")
                        print(seller_right_close.text)
                        actions.move_to_element(seller_right_close)
                        actions.click(seller_right_close)
                        actions.perform()
                        sleep(2)
                        #seller_main = driver.find_element(By.XPATH, "//div[@id='dp']")
                        # 设置一个最大等待时间，直到该元素被找到或者达到最大等待时间。
                        # 如果在最大等待时间内元素被找到了，则立即返回元素，并继续执行后面的代码。
                        # 如果超过最大等待时间，元素还未被找到，则抛出一个超时的异常。
                        seller_main = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@id='dp']")))
                        seller_info = seller_main.find_element(By.XPATH, ".//div[@class='quick-view-integrate-listing']")
                        seller_bar = seller_info.find_element(By.XPATH, ".//div[@class='tab-list d-flex align-items-center']")
                        seller_bar_list = seller_bar.find_elements(By.XPATH, "./div")
                        actions.move_to_element(seller_bar_list[0])
                        actions.click(seller_bar_list[0])
                        actions.perform()
                        sleep(1)
                        actions.move_to_element(seller_bar_list[1])
                        actions.click(seller_bar_list[1])
                        actions.perform()
                        sleep(1)
                    except Exception as e:
                        print(f'没有完成点击操作: {str(e)}') # type: ignore
            except Exception as e:
                print(f'没有完成验证码验证: {str(e)}') # type: ignore

#- 'int32','int64' - 整数型
#- 'float32','float64' - 浮点数型
#- 'str' - 字符串型
#- 'bool' - 布尔型
#- 'object' - 通用型
# DataFrame sheet_info的所有列的数据类型都转换为str
sheet_info = sheet_info.astype('object')
#for col in sheet_info.columns: #等同于
#    sheet_info[col] = sheet_info[col].astype('str')
#sheet_info['更新信息'] = sheet_info['更新信息'].astype(str)

options = webdriver.ChromeOptions()
options.binary_location = r'D:\Code\chrome-win\chrome.exe'
options.debugger_address = '127.0.0.1:9222'
options.browser_version = '114.0.5734.0'
#禁用Chrome浏览器的自动控制提示。当使用selenium开启Chrome浏览器时，浏览器的信息栏上方会有一条提示：“Chrome正在受到自动测试软件的控制”
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#禁用Selenium提供的自动化扩展。Selenium默认会载入一些用于自动化控制的浏览器扩展
#options.add_experimental_option('useAutomationExtension', False)
service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
#driver = webdriver.Chrome(service=service, options=options)设置超时时间20s，如果WebDriverException，
# 启动program_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# program_args = [
#        "--remote-debugging-port=9222",
#        "--user-data-dir=D:/Code/selenium/AutomationProfile",
#    ]的程序，且该程序只能存在一个
us_cookies=None
uk_cookies=None
driver = webdriver.Chrome(service=service, options=options)
#driver.get("https://www.amazon.com")
#us_cookies = driver.get_cookies()
#driver.get("https://www.amazon.co.uk")
#uk_cookies = driver.get_cookies()
wait = WebDriverWait(driver, 20)

driver.get("https://www.baidu.com")
driver.execute_script("window.open()") #通过执行JavaScript,在当前浏览器打开一个新的空白标签页。

def start_chrome_program():
    # 定义程序路径和参数
    program_path = "D:\\Code\\chrome-win\\chrome.exe"
    program_args = [
        "--remote-debugging-port=9222",
        "--user-data-dir=E:\\Code\\selenium\\AutomationProfile 114 Seller 9222",
    ]
    #subprocess.run()默认情况下是一个阻塞函数，它会等待子进程完成后才继续执行后面的代码。在你这个案例中，可能是因为浏览器在打开过程中，由于某种原因（比如网络连接）造成了程序的阻塞。
    #要解决这个问题，你可以将subprocess.run()替换为subprocess.Popen()，Popen()是一个非阻塞函数，一旦执行就会创建子进程并立即返回，而不会等待子进程结束。
    # 使用 subprocess 执行外部命令
    #subprocess.Popen([program_path] + program_args)
    shortcut_path = "D:\\Code\\chrome - New Selenium 2.lnk"
    os.startfile(shortcut_path)
    
    #subprocess.run(shortcut_path)
    sleep(10)

    return True

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
    #PylancereportOptionalMemberAccess
    #这个报错信息同样是由于self.driver可能为None导致的。之前的start_driver方法在尝试启动webdriver失败后，可能会返回None。然后你试图在None类型上调用 find_element 方法，这是不允许的。
    #一种解决办法是，在调用find_element方法之前，你可以检查self.driver是否已经被初始化。例如：
    '''if self.driver is not None:
        element = self.driver.find_element(By.ID, 'foo')
    else:
        print("Driver is not initialized. Can't find element.")'''
    #这样可以确保只有当driver被成功初始化后，才会进行元素查找。
    #另一种更深层次的解决办法是，你可以更改start_driver的设计，使得如果在超时时间内webdriver仍未成功启动，则抛出异常而不是返回None。

def OpenDriver(driver, wait, valurl: str):
    # 打开valurl网页
    for i in range(1,5):
        new_driver = None
        try:
            print(('driver.get(valurl)'))
            driver.get(valurl)
            return driver
        except Exception as e: 
            print(e)
            print(f'Exception occurred while getting page {valurl}, retrying {i+1} time')
            # 关闭可能打开的Chrome程序
            os.system('taskkill /f /im chrome.exe')
            # 启动新的Chrome程序
            start_chrome_program()
            sleep(2) # 等待2秒以确保程序启动
            # 重新启动driver
            #driver = self.start_driver()
            options = webdriver.ChromeOptions()
            options.binary_location = r'D:\Code\chrome-win\chrome.exe'
            options.debugger_address = '127.0.0.1:9222'
            options.browser_version = '114.0.5734.0'
            service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
            new_driver = webdriver.Chrome(service=service, options=options)
            new_driver.maximize_window()
            new_driver.get("https://www.baidu.com")
            new_driver.execute_script("window.open()")
            wait = WebDriverWait(new_driver, 30)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body'))) 
            # 如果driver启动失败，则抛出异常
            if new_driver is not None:
                driver = new_driver
            else:
                print(f"Failed to start driver within timeout: {i}.")
    # 1. 初始化WebDriverWait,设置最长等待时间为5秒:
    wait = WebDriverWait(driver, 30)
    # 2. 使用until方法设置等待条件:
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    # expected_conditions检查网页元素是否可见
    #condition=expected_conditions.visibility_of_element_located((By.ID,'kw'))
    #WebDriverWait(driver=driver,timeout=20,poll_frequency=0.5).until(condition)
    #!隐性等待，最长等待时间为30秒
    #driver.implicitly_wait(30)  


def GarbInfo(driver, wait,
        valurl: str, isSmallImg: bool, isBigImg: bool, is_Keepa: bool, is_Seller: bool
    ):
    driver = OpenDriver(driver, wait, valurl)
    wait = WebDriverWait(driver, 30)
    
    if driver is None:
        return None
    
    # 获取完整网页源码
    # source = driver.page_source
    # 打开文本文件并清空内容,将网页源码写入文本文件
    '''
    with open('page_source.txt', 'w', encoding='utf-8') as f:
        f.truncate()
        f.write(source)
    '''
    actions = ActionChains(driver)
    
    # 编译正则表达式提取ASIN
    asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
    # 从url1提取ASIN
    match = asin_pattern.search(valurl)
    ASIN = match[1] if match else None
    print(f'ASIN: {ASIN}')
    # 从url1提取国家代码
    Country = valurl.split('/')[2].split('.')[-1]
    if Country == 'com':
        Country = 'us'
    print(f'Country: {Country}')
    
    captcha_element_display(driver, '卖家精灵')
    
    # 1. 标题、价格 获取//*[@id="expandTitleToggle"]、//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1] 中的文本
    isRefresh = True
    title = ''
    flag = 1
    while isRefresh:
        try:
            title = driver.find_element(By.XPATH, '//*[@id="productTitle"]').text
        except Exception:
            print(('''driver.refresh()'''))
            isRefresh = True
            driver.refresh()
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
            sleep(5)
        else:
            isRefresh = False    
        flag = flag + 1
        if flag == 3:
            driver.execute_script("window.stop();")  # 网页停止加载的代码
            try:
                title = driver.find_element(By.XPATH, '//*[@id="productTitle"]').text
            except Exception:
                title = None
                print(('''ASIN ERROR'''))
            if title is None or title == '':
                return None
    
    print(title)
    
    sale_price = None
    rrp_price = None
    is_Deal = False
    discount = None
    # 检查是否可售
    try:
        # 检查是否在Deal //*[@id="dealBadge_feature_div"]/span/span/span
        temp = driver.find_element(
            By.XPATH, '//*[@id="dealBadge_feature_div"]/span/span/span'
        ).text
        is_Deal = temp == 'Deal'
    except Exception:
        is_Deal = False
        
    prime_price = None
    try:
        prime_element = driver.find_element(
            By.XPATH, '//*[@id="pep-signup-link"]/span[2]'
        )
        prime_price = prime_element.text
    except Exception:
        print('No prime price element found')
    else:
        print(f'prime price : {prime_price}')

    isAvailable = False
    try:
        unavailable_element = driver.find_element(
            By.XPATH, '//*[@id="availability"]/span'
        )
        # 转化成小写
        unavailable_text = unavailable_element.text.lower()
        print(unavailable_text)
    except Exception:
        isAvailable = True
    else:
        if 'unavailable' in unavailable_text:
            sale_price = 'Unavailable'
            isAvailable = False
        elif 'stock' in unavailable_text:
            isAvailable = True
            
    if isAvailable:
        try:
            # 检查是否有折扣标识
            # apex_desktop 下两级 有的是 apex_desktop_newAccordionRow 有的是 apex_desktop_qualifiedBuybox
            apex_element = driver.find_element(By.XPATH, '//*[@id="apex_desktop"]')
            corePrice_element = apex_element.find_element(
                By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]'
            )
            discount_element = corePrice_element.find_elements(
                By.XPATH,
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[contains(@class, "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")]',
            )[0]
            discount = discount_element.text
        except Exception:
            try:
                print('No discount info')
                # 无折扣,售价在第一个span
                # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]
                # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1]
                apex_element = driver.find_element(By.XPATH, '//*[@id="apex_desktop"]')
                sale_price_element = apex_element.find_element(
                    By.XPATH,
                    '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]',
                )
                driver.execute_script("arguments[0].className = ''; ", sale_price_element)
                sale_price = sale_price_element.text
            except Exception as e:
                print('=1=')
        else:
            if '%' in discount_element.text:
                try:
                    # 有折扣,售价在第二个span,原价在第四个span
                    sale_price_element = discount_element.find_element(
                        By.XPATH,
                        '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[1]',
                    )
                    # 删除class="a-offscreen"
                    driver.execute_script(
                        "arguments[0].className = ''; ", sale_price_element
                    )
                    # 再次获取text,此时可以获得正确值
                    sale_price = sale_price_element.text
                    #//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span/span[1]
                    rrp_price_element = discount_element.find_element(
                        By.XPATH,
                        '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[1]',
                    )
                    driver.execute_script(
                        "arguments[0].className = ''; ", rrp_price_element
                    )
                    rrp_price = rrp_price_element.text
                except Exception as e:
                    print('=1=')
            else:
                try:
                    print('No discount info')
                    # 无折扣,售价在第一个span
                    apex_element = driver.find_element(By.XPATH, '//*[@id="apex_desktop"]')
                    sale_price_element = apex_element.find_element(
                        By.XPATH,
                        '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1]',
                    )
                    driver.execute_script(
                        "arguments[0].className = ''; ", sale_price_element
                    )
                    sale_price = sale_price_element.text
                except Exception as e:
                    print('=1=')
                    
        print(f'Is In Deal: {is_Deal}')
        print(f'Sale Price: {sale_price}')
        print(f'RRP Price: {rrp_price}') if rrp_price else print('No RRP Price')
        print(f'Discount off: {discount}')

    # 2. 评分、评论数 父元素//*[@id="averageCustomerReviews"],获取//*[@id="acrPopover"]/span[1]/a/span 文本,获取//*[@id="acrCustomerReviewText"]文本
    rating = ''
    review = ''
    try:
        parent = driver.find_element(By.XPATH, '//*[@id="averageCustomerReviews"]')
        rating = parent.find_element(
            By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span'
        ).text
        
        review = parent.find_element(By.XPATH, '//*[@id="acrCustomerReviewText"]').text
        
    except Exception:
        print('No rating review element found')
    else:
        try:
            review = review.replace('ratings', '').strip()
        except Exception:
            print('')
        print(f'rating : {rating}')
        print(f'review : {review}')

    # 2.1 品牌获取//*[@id="bylineInfo"]的文本,并用空格分割字符串
    brand = ''
    try:
        brand = driver.find_element(By.ID, 'bylineInfo').text
        # 过滤字符串
        brand = brand.replace(':', '')  # 去除冒号
        brand = brand.replace('Visit the', '')  # 去除Visit the
        brand = brand.replace('Store', '')  # 去除Store
        brand = brand.replace('Brand', '')  # 去除Brand:
        brand = brand.strip()  # 去除首尾空格
        print(brand)
    except Exception:
        print('No brand element found')
    else:
        print(f'brand : {brand}')

    # 2.2 变体
    variant_info = []
    try:
        variant_element = driver.find_element(By.ID, 'twister_feature_div')
        variant_divs = variant_element.find_elements(
            By.XPATH,
            './/div[contains(@class, "twisterSwatchWrapper_0 twisterSwatchWrapper twisterImages thinWidthOverride")]',
        )
        for variant_div in variant_divs:
            # ./ancestor::li[1] 来相对于 variant_div 元素查找最近的 li 父元素
            li_element = variant_div.find_element(By.XPATH, './ancestor::li[1]')
            variant_ASIN = li_element.get_attribute('data-defaultasin')
            # 添加了一个.，表示相对于variant_div元素进行定位。这样可以确保XPath表达式在当前variant_div元素的上下文中执行，而不是全局执行。
            # variant_name = variant_div.find_element(By.XPATH,'.//div[1]/img').get_attribute('src')
            # variant_img = variant_div.find_element(By.XPATH,'.//div[1]/img').get_attribute('src')
            # variant_price = variant_div.find_element(By.XPATH,'.//div[2]/div/span/p').text
            variant_name = ''
            try:
                variant_name = variant_div.find_element(
                    By.XPATH, './/div[contains(@class, "twisterTextDiv")]//p[last()]'
                ).text
            except Exception:
                print('No variant_name found')
            variant_img = ''
            try:
                variant_img = variant_div.find_element(
                    By.XPATH, './/div[contains(@class, "twisterImageDiv")]//img[last()]'
                ).get_attribute('src')
            except Exception:
                print('No variant_img found')
            variant_price = variant_div.find_element(
                By.XPATH, './/div[contains(@class, "twisterSlotDiv")]//p[last()]'
            ).text
            print(
                f'variant_ASIN:{variant_ASIN}====variant_img:{variant_img}=====variant_price:{variant_price}'
            )
            variant_info.append(
                {
                    'ASIN': variant_ASIN,
                    'name': variant_name,
                    'img': variant_img,
                    'price': variant_price,
                }
            )
    except Exception:
        print('No variant element found')
    else:
        variant_count = len(variant_divs)
        print(f'variant_info : {variant_info}')
        print(f'variant_count : {variant_count}')

    coupon = None
    saving = None
    promotion = None
    # 3.1 找到父元素//*[@id="promoPriceBlockMessage_feature_div"]
    parent = driver.find_element(
        By.XPATH, '//*[@id="promoPriceBlockMessage_feature_div"]'
    )
    try:
        # 3.2 优惠券 找到子元素1//*[@id="couponTextpctch*"](用contain匹配)
        coupon = parent.find_element(
            By.XPATH, '//*[@id[contains(., "couponTextpctch")]]'
        ).text
        # coupon = coupon.replace('|', '')
        # coupon = coupon.replace('Terms', '')
        # coupon = coupon.strip()
        coupon = re.findall(r'[\d%]+', coupon)
    except Exception:
        print('No coupon element found')
    else:
        print(f'coupon : {coupon}')

    try:
        # 3.3 优惠2a 找到子元素2//*[@id="couponBadgepctch*"](用contain匹配)
        saving_a = parent.find_element(
            By.XPATH, '//*[@id[contains(., "couponBadgepctch")]]'
        ).text
        # 3.4 优惠2b 找到子元素3//*[@id="promoMessagepctch*"](用contain匹配)
        saving_b = parent.find_element(
            By.XPATH, '//*[@id[contains(., "promoMessagepctch")]]'
        ).text
        saving = f"{saving_a} {saving_b}"
        saving = saving.replace('|', '')
        saving = saving.replace('Terms', '')
        saving = saving.strip()
    except Exception:
        print('No saving element found')
    else:
        print(f'saving : {saving}')

    try:
        # 父元素//*[@id="applicablePromotionList_feature_div"] 与优惠1 2 不同
        # 3.3 优惠券3 找到元素//*[@id="applicable_promotion_list_sec"]/span/span/a/span[2]/span[1]
        parent = driver.find_element(
            By.XPATH, '//*[@id="applicablePromotionList_feature_div"]'
        )
        promotion_a = parent.find_element(
            By.XPATH,
            '//*[@id="applicable_promotion_list_sec"]/span/span/a/span[2]/span[1]',
        ).text
        promotion_b = parent.find_element(
            By.XPATH,
            '//*[@id="applicable_promotion_list_sec"]/span/span/a/span[2]/span[2]',
        ).text
        promotion = f"{promotion_a} {promotion_b}"
        promotion = promotion.replace('|', '')
        promotion = promotion.replace('Terms', '')
        promotion = promotion.strip()
    except Exception:
        print('No promotion element found')
    else:
        print(f'promotion : {promotion}')

        # 4.1 获取Amazon's Choice
    amz_choice = None
    try:
        amz_choice = driver.find_element(
            By.XPATH, '//*[@id="acBadge_feature_div"]/div/span[2]/span/span/a'
        ).text
    except Exception:
        print('No Amazon Choice element found')
    else:
        print(f'Amazon Choice : {amz_choice}')

        # 4.2 五点描述 找到父元素//*[@id="feature-bullets"],获取父元素下//*[@id="feature-bullets"]/ul/li 的li中的文本,保存为数组
    bullet_points = []
    try:
        parent = driver.find_element(By.XPATH, '//*[@id="feature-bullets"]/ul')
    except Exception:
        print('No bullet_points element found')
    else:
        lis = parent.find_elements(By.XPATH, './/li')
        for li in lis:
            bullet_points.append(li.text)
        print(f'bullet_points : {bullet_points}')

    # 5. 获取table //*[@id="productOverview_feature_div"]中的信息,用字典保存
    base_info = {}
    try:
        parent = driver.find_element(
            By.XPATH, '//*[@id="productOverview_feature_div"]/div/table'
        )
        trs = parent.find_elements(By.XPATH, './/tbody/tr')
        for tr in trs:
            key = tr.find_element(By.XPATH, 'td[1]').text
            value = tr.find_element(By.XPATH, 'td[2]').text
            base_info[key] = value
    except Exception:
        print('No Basic Info element found')
    else:
        print(f'Basic Info : {base_info}')

        # 6. 获取table //*[@id="productDetails_techSpec_section_1"]中的信息,用字典保存
    dict_data_Details = {}
    try:
        table1 = driver.find_element(
            By.XPATH, '//*[@id="productDetails_techSpec_section_1"]'
        )
        for tr in table1.find_elements(By.TAG_NAME, 'tr'):
            th = tr.find_element(By.TAG_NAME, 'th')
            td = tr.find_element(By.TAG_NAME, 'td')
            key = th.text
            value = td.text
            dict_data_Details[key] = value
    except Exception:
        print('No dict_data_Details element found')
    else:
        print(f'dict_data_Details : {dict_data_Details}')

        # 7. 获取table //*[@id="productDetails_detailBullets_sections1"] 中的信息,用字典保存
    dict_data_Info = {}
    try:
        table2 = driver.find_element(
            By.XPATH, '//*[@id="productDetails_detailBullets_sections1"]'
        )
        for tr in table2.find_elements(By.TAG_NAME, 'tr'):
            th = tr.find_element(By.TAG_NAME, 'th')
            td = tr.find_element(By.TAG_NAME, 'td')
            key = th.text
            value = td.text
            dict_data_Info[key] = value
    except Exception:
        print('No dict_data_Info element found')
    else:
        print(f'dict_data_Info : {dict_data_Info}')
        
    if is_Keepa:
        try:
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]')))
            seller_parent = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]')
            seller_Linechart = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]/div[2]/div/div[1]/div[1]/div[2]/span')
            actions.move_to_element(seller_Linechart)
            actions.click(seller_Linechart)
            actions.perform()
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div/div[1]/canvas')))
            seller_canvas = seller_parent.find_element(By.XPATH, './/canvas')
            # //*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div[2]/div
            try:
                wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div[2]/div')))
                seller_selector = WebDriverWait(seller_parent, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'rang-div')))
            except Exception as e:
                print(str(e))
            seller_selector = seller_parent.find_element(By.CLASS_NAME,'rang-div')
            seller_selector_p = seller_selector.find_elements(By.TAG_NAME,'p')
            if seller_selector_p[-2].find_element(By.XPATH,'./span').text == '最近一年':
                actions.move_to_element(seller_selector_p[-2])
                actions.click(seller_selector_p[-2])
                actions.perform()
            else:
                actions.move_to_element(seller_selector_p[-1])
                actions.click(seller_selector_p[-1])
                actions.perform()
            #folder = r'D:\AutoRPA\卖家精灵\ASIN'
            #asin_folder = folder.replace('ASIN', str(ASIN))
            folder = f'D:\\AutoRPA\\卖家精灵\\{ASIN}'
            if not os.path.exists(folder):
                os.makedirs(folder)
            seller_canvas.screenshot(f'{folder}\\seller_canvas.png')
            seller_quickiew = driver.find_element(By.XPATH,'//*[@id="seller-sprite-extension-quick-view-listing"]')
            # 获取元素的x,y坐标
            x = seller_quickiew.location['x']
            y = seller_quickiew.location['y']
            # 滚动页面,使元素顶部与页面顶部对齐
            driver.execute_script(f"window.scrollTo(0, {y});")
            # 截取指定区域
            driver.get_screenshot_as_file('screenshot.png')
            img = Image.open('screenshot.png')
            # 将元素顶部与页面顶部对齐后，y=0
            img = img.crop((x, 0, x+550, 290)) 
            img.save(f'{folder}\\seller_quickview.png')
            #!
            #sheet_array.loc[index, 'isKeepa'] = False
        except Exception as e:
            print(f'No Seller element found:{str(e.msg)}') # type: ignore

        # 8. 图片 父元素//*[@id="altImages"]/ul
    # 循环点击左边的小图
    ul = driver.find_element(By.XPATH, '//*[@id="altImages"]/ul')
    image_left1 = None
    # 获取所有450尺寸的主图链接
    image_main450 = []
    if isSmallImg:
        for li in ul.find_elements(By.TAG_NAME, 'li'):
            # 如果li的class包含template或aok-hidden或videoThumbnail,继续下一个循环
            if (
                'template' in li.get_attribute('class')  # type: ignore
                or 'aok-hidden' in li.get_attribute('class')  # type: ignore
                or 'videoThumbnail' in li.get_attribute('class')  # type: ignore
                or 'sellersprite' in li.get_attribute('id')  # type: ignore
                or 'pos-360' in li.get_attribute('class')  # type: ignore
            ):
                continue
            span = li.find_element(By.XPATH, './span/span')
            actions.move_to_element(span)
            actions.click(span)
            actions.perform()
            sleep(1)
        ul = driver.find_element(By.XPATH, '//*[@id="main-image-container"]/ul')
        for li in ul.find_elements(By.XPATH, 'li'):
            if 'image' in li.get_attribute('class') and 'item' in li.get_attribute( # type: ignore
                    'class'
            ): # type: ignore
                img = li.find_element(By.XPATH, './span/span/div/img')
                img_src = img.get_attribute('src')
                image_main450.append(img_src)
        print(image_main450)

    # 遍历父元素下所有元素
    elements = []

    def get_elements(parent):
        children = parent.find_elements(By.XPATH, './*')
        for child in children:
            elements.append(child)
            get_elements(child)
        return elements

    # 8.1 获取视频数量
    video_count = 0
    try:
        video_text = driver.find_element(By.XPATH, '//*[@id="videoCount"]').text.strip()
        if video_text == "VIDEO":
            video_count = 1
        elif video_text == "VIDEOS":
            video_count = 1
        elif 'VIDEOS' in video_text:
            # \d+ 表示匹配一个或多个数字,这是一个正则表达式,而不是一个字符串。所以这里使用转义序列 \d 是正确的,不会产生无效的转义序列错误。
            # 但是,Pylance 分析器误以为这是一个字符串,所以报告了无效的转义序列错误。
            # 在字符串开头添加 r 会让 Pylance 知道这是一个原始字符串,实际上是正则表达式,可以安全地使用转义序列。
            numbers = re.findall(r'\d+', video_text)
            video_count = int(''.join(numbers))
    except Exception:
        print('No videoCount element found')
    else:
        print(f'videoCount : {video_count}')
        
    if is_Seller:
        try:
            seller_parent = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]')
            # 回滚至顶部
            driver.execute_script("window.scrollTo(0, 0);")
            # 使用图像识别
            seller_chart = seller_parent.find_element(By.XPATH, ".//div[@class='quick-view-integrate-listing']")
            seller_canvas = seller_chart.find_element(By.XPATH, ".//canvas")
            # 截屏并处理
            screenshot = driver.get_screenshot_as_png()
            screenshot = Image.open(BytesIO(screenshot))
            # 截取特定元素的部分
            location = seller_canvas.location
            size = seller_canvas.size
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            screenshot = screenshot.crop((left, top, right, bottom))
            # 匹配图像
            template_path = 'D:\\Code\\# OUTPUT\\Amazon_Refactor\\image\\download.png'  # 替换成你的模板图像路径
            screenshot_array = np.array(screenshot)
            template = cv2.imread(template_path,0)
            res = cv2.matchTemplate(cv2.cvtColor(screenshot_array, cv2.COLOR_BGR2GRAY), template, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(res)
            x, y = max_loc
            # 点击操作
            template_width, template_height = template.shape[::-1]  # 获取模板的宽度和高度
            center_x = x + template_width / 2  # 计算模板中心的 x 坐标
            center_y = y + template_height / 2  # 计算模板中心的 y 坐标
            # 在识别出的位置画红点
            #screenshot_array = cv2.circle(screenshot_array, (center_x, center_y), radius=5, color=(0, 0, 255), thickness=-1)
            # 保存图像到指定位置
            #output_path = 'D:\\Code\\# OUTPUT\\Amazon_Refactor\\output.png' # 替换为你的路径
            #cv2.imwrite(output_path, screenshot_array)
            
            #actions = webdriver.ActionChains(driver)
            #relative_x = center_x - location['x']
            #relative_y = center_y - location['y']
            # 使用 '//' 符号进行整数（向下）除法运算，其结果将直接被转化为整数，这意味着除法运算结果的小数部分被“舍去”。
            # 而使用 '/' 符号进行除法运算时，即便两个操作数都是整数，其结果也会是浮点数（即保留小数部分）
            # selenium版本4.4.3move_to_element_with_offset是基于中心点
            halfWidth = seller_canvas.size['width'] / 2
            halfHeight = seller_canvas.size['height'] / 2
            relative_x = center_x - halfWidth 
            relative_y = center_y - halfHeight
            actions.move_to_element_with_offset(seller_canvas, relative_x, relative_y)
            actions.click()
            actions.perform()
            print("点击下载")
            # 通过JavaScript代码在网页上画红点
            absolute_x = left + center_x
            absolute_y = top + center_y
            
            
            script_old = """
            var element = document.elementFromPoint({absolute_x}, {absolute_y}); // 获取指定位置的元素
            var clickEvent= document.createEvent('MouseEvents'); // 创建一个点击事件
            clickEvent.initMouseEvent(
                'click', true, true, window, 0, 0, 0, {absolute_x}, {absolute_y}, false, false,
                false, false, 0, null
            ); // 初始化点击事件
            element.dispatchEvent(clickEvent); // 派发点击事件
            """
            script_old2 = f"""
            var evt = new MouseEvent('click', {{
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: {absolute_x},
                clientY: {absolute_y}
            }});
            document.elementFromPoint({absolute_x}, {absolute_y}).dispatchEvent(evt);
            """
            #script = script.format(absolute_x=absolute_x, absolute_y=absolute_y) # Python中格式化JavaScript代码
            #driver.execute_script(script) # 执行JavaScript代码
            # 用execute_script执行JS代码
            '''driver.execute_script("""
                function simulateClick(x, y) {
                    var clickEvent = new MouseEvent('click', {
                        'view': window,
                        'bubbles': true,
                        'cancelable': true,
                        'clientX': x,
                        'clientY': y
                    });
                    document.elementFromPoint(x, y).dispatchEvent(clickEvent);
                }
                simulateClick(arguments[0], arguments[1]);
            """, absolute_x, absolute_y)  # 在页面的(100, 200)位置模拟一次点击'''
            driver.execute_script("""
                var x = arguments[0];
                var y = arguments[1];
                function simulateClick(x, y) {
                    var event = new MouseEvent('click', {
                        clientX: x,
                        clientY: y,
                        button: 0,  // 0 表示鼠标左键
                        buttons: 1,  // 1 表示鼠标左键按下
                        view: window
                    });
                    document.elementFromPoint(x, y).dispatchEvent(event);
                }
                simulateClick(x, y);
            """, absolute_x, absolute_y)
            
            
            script = f"var ele = document.createElement('div');" \
                    f"ele.style.position = 'fixed';" \
                    f"ele.style.left = '{absolute_x}px';" \
                    f"ele.style.top = '{absolute_y}px';" \
                    f"ele.style.width = '10px';" \
                    f"ele.style.height = '10px';" \
                    f"ele.style.background = 'red';" \
                    f"document.body.appendChild(ele);"
            driver.execute_script(script)
            sleep(2)
            
            # 卖家精灵图标
            '''seller_logo = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]/div[1]/div[1]/a/img')
            # 悬停至元素上
            actions.move_to_element(seller_logo)
            actions.perform()
            location = seller_parent.location
            size = seller_parent.size
            print(location)
            print(size)
            actions = ActionChains(driver)
            # 相对与当前位置偏移
            actions.move_by_offset(1412, 180)
            actions.click()
            actions.perform()
            time.sleep(2)'''
            # 如何处理下载失败？\
            # !
            #sheet_array.loc[index, 'isSeller'] = False
        except Exception as e:
            print(f'No Rank Download Fialure element found:{str(e.msg)}')# type: ignore

    image_main1500 = []
    # 9. 如果参数isBigImg为真，获取1000+的大尺寸主图
    if isBigImg:
        try:
            # 先点击第一张主图(侧边栏)
            # image_left1 = driver.find_element(By.XPATH, '//*[@id="a-autoid-6"]')
            actions.move_to_element(image_left1)
            actions.click(image_left1)
            actions.perform()
            # 找到图片弹窗元素,模拟点击 //*[@id="imgTagWrapperId"]无法被点击？
            # 部分ASIN 没有[@id="landingImage"] 有class=landingImage
            main_image_element = driver.find_element(
                By.XPATH, '//*[@id="main-image-container"]'
            )
            image_popup = main_image_element.find_element(
                By.XPATH, './/div[@class="imgTagWrapper"]/img'
            )
            # image_popup = driver.find_element(By.XPATH, '//*[@id="landingImage"]')
            actions.move_to_element(image_popup)
            actions.click(image_popup)
            actions.perform()

            # 等待a-popover-content元素出现 //*[@id="ivImagesTabHeading"]/a
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ivImagesTabHeading"]/a')
                )
            )

            # 找到父元素,和子元素div class="ivRow"
            parent = driver.find_element(By.XPATH, '//*[@id="ivThumbs"]')
            divs = parent.find_elements(By.XPATH, './/div[@class="ivRow"]')
            elements = []
            for div in divs:
                des_div = div.find_elements(By.XPATH, './div')
                for ddiv in des_div:
                    elements.append(ddiv)

            # 依次点击elements中的元素,并获取图片链接
            for element in elements:
                actions.move_to_element(element)
                actions.click(element)
                actions.perform()
                time.sleep(0.5)
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="ivLargeImage"]/img')
                    )
                )
                img = driver.find_element(By.XPATH, '//*[@id="ivLargeImage"]/img')
                img_url = img.get_attribute('src')
                while 'loading' in img_url:  # type: ignore
                    time.sleep(0.5)
                    img_url = img.get_attribute('src')
                image_main1500.append(img_url)

            time.sleep(2)
            
            # 添加点击左上角向下偏移200位置
            
            '''image_close = driver.find_element(
                By.XPATH,
                '//button[contains(@class, "a-button-close") and @data-action="a-popover-close" and not(contains(@class, "vse-close-button"))]',
            )
            actions.move_to_element(image_close)
            actions.click(image_close)
            actions.perform()'''
            
            time.sleep(1)
        except Exception:
            print('No description element found')
        else:
            print(f'image_main1500 : ,{image_main1500}')

    time.sleep(2)
    
    # 网页截图
    if is_Keepa:
        print('Keeepa截图')

    if is_Seller:
        print('Seller截图')

    # 10. 获取详情页的文本和图片链接
    # 20230720:先进行读取所有文本，再进行除重，最后合成文本
    description = []
    image_description = []
    img_src = ''
    description_srt = ''
    try:
        parent = driver.find_element(By.XPATH, '//*[@id="aplus_feature_div"]')
        elements = get_elements(parent)
        for element in elements:
            if (
                element.tag_name == 'p'
                or element.tag_name.startswith('h')
                or element.tag_name.startswith('h1')
                or element.tag_name.startswith('h2')
                or element.tag_name.startswith('h3')
                or element.tag_name.startswith('h4')
                or element.tag_name.startswith('h5')
                or element.tag_name == 'span'
            ):
                description.append(element.text)
            elif element.tag_name == 'img':
                img_src = element.get_attribute('data-src')
            if img_src:
                image_description.append(img_src)

    except Exception:
        print('No description element found')
    else:
        # 去除重复的元素
        image_description = remove_duplicates(image_description)

        description_srt = ''
        for item in description:
            if item == '':
                continue
            description_srt += item + '\n'
        description_srt = description_srt.strip()
        print(f'description_srt : {description_srt}')
        print(f'image_description : ,{image_description}')
        
    sleep(2)
    # 关闭当前标签页
    #driver.close()

    # 打包成字典
    AMZInfoDict = {}
    AMZInfoDict['链接'] = valurl
    AMZInfoDict['ASIN'] = ASIN
    AMZInfoDict['国家'] = Country
    AMZInfoDict['标题'] = title
    AMZInfoDict['变体'] = variant_info
    AMZInfoDict['isDeal'] = is_Deal
    AMZInfoDict['现价'] = sale_price
    AMZInfoDict['RRP'] = rrp_price
    AMZInfoDict['会员价'] = prime_price
    AMZInfoDict['折扣'] = discount
    AMZInfoDict['评分'] = rating
    AMZInfoDict['评价数'] = review
    AMZInfoDict['品牌'] = brand
    AMZInfoDict['coupon'] = coupon
    AMZInfoDict['saving'] = saving
    AMZInfoDict['promotion'] = promotion
    AMZInfoDict['AmazonChoice'] = amz_choice
    AMZInfoDict['五点描述'] = bullet_points
    AMZInfoDict['展示信息'] = base_info
    AMZInfoDict['产品信息'] = dict_data_Details
    AMZInfoDict['商品信息'] = dict_data_Info
    AMZInfoDict['主图450'] = image_main450
    AMZInfoDict['视频数量'] = video_count
    AMZInfoDict['主图1500'] = image_main1500
    AMZInfoDict['视频数量'] = video_count
    AMZInfoDict['详情描述'] = description_srt
    AMZInfoDict['详情图片'] = image_description
    return AMZInfoDict


def remove_duplicates(nums):
    # 使用集合的特性,将数组转换为集合,重复元素会被自动去除
    nums_set = set(nums)
    # 将集合转换回列表
    return list(nums_set)

for index, (row_index, row) in enumerate(sheet_array.iterrows(),start=2):
    url = None if pd.isna(row['链接']) else row['链接']  # 链接地址
    updateTime = False if pd.isna(row['更新时间']) else row['更新时间']   # 是否更新(日期) # 45090 指 2023/6/13
    updateCycle = False if pd.isna(row['更新周期']) else int(row['更新周期'])  # 主图450(整数型)
    isUpdate = False if pd.isna(row['是否更新']) else bool(row['是否更新'])  # 是否更新(布尔型)
    isSmallImg = False if pd.isna(row['主图450']) else bool(row['主图450'])  # 主图450(布尔型)
    isBigImg = False if pd.isna(row['主图1500']) else bool(row['主图1500'])  # 主图1500(布尔型)
    isKeepa = False if pd.isna(row['isKeepa']) else bool(row['isKeepa'])  # isKeepa(布尔型)
    isSeller = False if pd.isna(row['isSeller']) else bool(row['isSeller'])  # isSeller(布尔型)
    ### 添加更新时间判断

    result = {}
    if url and isUpdate:
        result = GarbInfo(driver, wait, url, isSmallImg, isBigImg, isKeepa, isSeller)  # type: ignore
    else:
        continue
    if result is not None:
        if 'sspa' in url:
            asin_pattern = re.compile(r'dp%2F([A-Za-z0-9]{10})')
        else:
            asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
        match = asin_pattern.search(url)
        asin = match[1] if match else None
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        domain_parts = domain.split('.')
        if len(domain_parts) >= 4:
            domain_suffix = f'{domain_parts[-2]}.{domain_parts[-1]}'
        else:
            domain_suffix = domain_parts[-1]
        domain_suffix_country_dict = {'com': 'us', 'co.uk': 'uk'}
        country = domain_suffix_country_dict.get(domain_suffix, domain_suffix)
        new_url = f'https://{domain}/dp/{asin}'

        ASIN = result.get('ASIN')
        主图450 = result.get('主图450')
        主图1500 = result.get('主图1500')
        详情图片 = result.get('详情图片')
        picture_file_path = config['picture_file_path']
        image_dir = f'{picture_file_path}/{ASIN}/'
        if isSmallImg and 主图450 is not None:
            picdownload(us_cookies,uk_cookies,new_url,ASIN,country, 主图450, image_dir, '450')  # type: ignore[arg-type]
            #def picdownload(url, asin, country, img_list: list, image_dir, filename):

        #if isBigImg and 主图1500 is not None:
        #    picdownload(ASIN, 主图1500, image_dir, '1500')  # type: ignore[arg-type]

        #if 详情图片 is not None:
        #    picdownload(ASIN, 详情图片, image_dir, '详情')  # type: ignore[arg-type]

        pdupdate(sheet_info, result, sheet_info_path)
        #sheet_array.loc[index, '是否更新'] = False
        #sheet_array.to_excel(sheet_array_path, index=False)

        time.sleep(5)

#sheet_info = pdformat(sheet_info)
sheet_info.to_excel(sheet_info_path, index=False)

