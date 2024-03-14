import os
import time
import re
import json
import yaml
from datetime import datetime

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup

from collections import defaultdict

from docx import Document
import logging

from PIL import Image
from PIL import Image

from Tool.Tool_Web import *
from Tool.Tool_Data import *
from Tool.Tool_SQL import *


class AmazonSearch:
    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait, actions: ActionChains
    ):
        self.driver, self.wait, self.actions = driver, wait, actions
        self.static_value()
        
        # 获取当前时间并将其转换为字符串
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 根据当前时间创建.log文件的名称
        self.logfilename = f"log_{current_time}.txt"
        # 获取当前目录的路径（也就是你的脚本所在的目录）
        self.logfileroot = os.path.dirname(os.path.abspath(__file__))
        # 将目录和文件名结合，获得完整的文件路径
        self.logfilename = os.path.join(
            self.logfileroot, self.logfilename
        )
        # 配置日志记录器
        logging.basicConfig(
            filename=self.logfilename,
            level=logging.DEBUG,
            # 在日志中记录内容，而不记录时间，可以在logging.basicConfig函数的format参数中只保留%(message)s，而去掉%(asctime)s -
            format='%(message)s'
            #format='%(asctime)s - %(message)s',
            #datefmt='%Y-%m-%d %H:%M:%S'
        )
        # 使用日志记录器
        logging.info('## This is a Garb_Search message')
        #logging.error('This is an error message')
        
    def static_value(self):
        self.savelog = True
        self.seller = True
        self.country = None
        self.info_all_count = 0
        self.info_fail_count = 0
        self.asin_all_count = 0
        self.asin_fail_count = 0
        self.div_class_list = list()
        self.section_dict = {}

        self.sql = MysqlUtil()

        # 品牌广告
        # _c2Itd_cardContainer_27VO-
        self.result_class_SB = (
            's-result-item s-widget s-widget-spacing-large AdHolder s-flex-full-width'
        )
        # 自然结果
        #                       sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20
        self.result_class_NR = 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'
        # 商品广告
        #                       sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20
        self.result_class_SP = 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20'
        # 高评价推荐 Trending now
        #                       sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom sg-col-12-of-16 s-widget-spacing-large
        self.result_class_HR = 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom sg-col-12-of-16 s-widget-spacing-large'
        # 视频广告
        #                       sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom s-widget-spacing-small sg-col-12-of-16
        self.result_class_BV = 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom s-widget-spacing-small sg-col-12-of-16'
        # 搜索结果抬头标题 index =1 or 2  (index=0 品牌广告时)
        # a-section a-spacing-none s-result-item s-flex-full-width s-border-bottom-none s-widget s-widget-spacing-large

    # 调试时，每次get_Search都运行一次
    def info_init(self):
        self.asin = None
        self.asin_url = None  # 点击后跳转的url链接？
        self.image = None
        self.title = None
        self.amz_choice = None
        self.best_seller = None
        self.variant = None
        self.variant_type = None
        self.variant_count = None
        self.deal_type = None
        self.is_deal = None  # boolean value
        self.fba = None
        self.is_fba = None  # boolean value
        self.is_amz = None  # boolean value
        self.is_smb = None  # boolean value
        self.left_count = None  # TINYINT
        self.lower_price = None
        self.lower_list = None
        self.lowest_precent = None
        self.sale_price = None
        self.rrp_price = None
        self.rrp_type = None
        self.prime_price = None
        self.discount = None
        self.coupon = None
        self.saving = None
        self.promotion = None
        self.promotion_code = None
        self.rating = None
        self.review = None
        self.bought = None
        self.a_rank_name = None
        self.a_rank = None
        self.b_rank_name = None
        self.b_rank = None
        self.c_rank_name = None
        self.c_rank = None
        self.d_rank_name = None
        self.d_rank = None

        # 长期不会更改
        self.brand = None
        self.merchant_token = None
        self.use_age = None
        self.use_ages_do = None
        self.use_ages_up = None
        self.bullet_points_1 = None
        self.bullet_points_2 = None
        self.bullet_points_3 = None
        self.bullet_points_4 = None
        self.bullet_points_5 = None
        self.bullet_points_6 = None
        self.bullet_points = None
        self.base_info = None
        self.weight = None
        self.weight_unit = None
        self.length_l = None
        self.length_w = None
        self.length_h = None
        self.length_unit = None
        self.start_sale_time = None
        
        # 西柚数据
        self.xiyou_seven_days_views =None
        self.xiyou_na_ratio = None
        self.xiyou_ad_ratio = None

        # 实时变化
        self.data_index = None
        self.data_uuid = None
        self.data_component_type = None
        self.data_component_id = None
        self.data_cel_widget = None
        self.data_type = None

        self.time = None

        #return self
    
    # 输出所有字典信息
    def to_all_dict(self):
        return {
            "asin": self.asin,
            "asin_url": self.asin_url,
            "image": self.image,
            "title": self.title,
            "amz_choice": self.amz_choice,
            "best_seller": self.best_seller,
            "variant": self.variant,
            "variant_type": self.variant_type,
            "variant_count": self.variant_count,
            "deal_type": self.deal_type,
            "is_deal": self.is_deal,
            "fba": self.fba,
            "is_fba": self.is_fba,
            "is_amz": self.is_amz,
            "is_smb": self.is_smb,
            "left_count": self.left_count,
            "lower_price": self.lower_price,
            "lower_list": self.lower_list,
            "lowest_precent": self.lowest_precent,
            "sale_price": self.sale_price,
            "rrp_price": self.rrp_price,
            "rrp_type": self.rrp_type,
            "prime_price": self.prime_price,
            "discount": self.discount,
            "coupon": self.coupon,
            "saving": self.saving,
            "promotion": self.promotion,
            "rating": self.rating,
            "review": self.review,
            "bought": self.bought,
            "a_rank_name": self.a_rank_name,
            "a_rank": self.a_rank,
            "b_rank_name": self.b_rank_name,
            "b_rank": self.b_rank,
            "c_rank_name": self.c_rank_name,
            "c_rank": self.c_rank,
            "d_rank_name": self.d_rank_name,
            "d_rank": self.d_rank,
            "brand": self.brand,
            "merchant_token": self.merchant_token,
            "use_age": self.use_age,
            "use_ages_do": self.use_ages_do,
            "use_ages_up": self.use_ages_up,
            "bullet_points_1": self.bullet_points_1,
            "bullet_points_2": self.bullet_points_2,
            "bullet_points_3": self.bullet_points_3,
            "bullet_points_4": self.bullet_points_4,
            "bullet_points_5": self.bullet_points_5,
            "bullet_points_6": self.bullet_points_6,
            "bullet_points": self.bullet_points,
            "base_info": self.base_info,
            "weight": self.weight,
            "weight_unit": self.weight_unit,
            "length_l": self.length_l,
            "length_w": self.length_w,
            "length_h": self.length_h,
            "length_unit": self.length_unit,
            "start_sale_time": self.start_sale_time,
            "data_index": self.data_index,
            "data_uuid": self.data_uuid,
            "data_component_type": self.data_component_type,
            "data_component_id": self.data_component_id,
            "data_cel_widget": self.data_cel_widget,
            "data_type": self.data_type,
            "xiyou_seven_days_views":self.xiyou_seven_days_views,
            "xiyou_na_ratio":self.xiyou_na_ratio,
            "xiyou_ad_ratio":self.xiyou_ad_ratio,
            "time": self.time
        }

    # 输出数据库info_current的对应字典
    def to_info_current_dict(self):
        return {
            "asin": self.asin,
            "country": self.country,
            "time": self.time,
            "image": self.image,
            "title": self.title,
            "brand": self.brand,
            "merchant_token": self.merchant_token,
            "amz_choice": self.amz_choice,
            "best_seller": self.best_seller,
            "deal_type": self.deal_type,
            "is_deal": self.is_deal,
            "is_fba": self.is_fba,
            "is_amz": self.is_amz,
            "is_smb": self.is_smb,
            "left_count": self.left_count,
            "lower_price": self.lower_price,
            "lower_list": self.lower_list,
            "lowest_precent": self.lowest_precent,
            "sale_price": self.sale_price,
            "rrp_price": self.rrp_price,
            "rrp_type": self.rrp_type,
            "prime_price": self.prime_price,
            "discount": self.discount,
            "coupon": self.coupon,
            "saving": self.saving,
            "promotion": self.promotion,
            "promotion_code": self.promotion_code,
            "rating": self.rating,
            "review": self.review,
            "bought": self.bought,
            "a_rank_name": self.a_rank_name,
            "a_rank": self.a_rank,
            "b_rank_name": self.b_rank_name,
            "b_rank": self.b_rank,
            "c_rank_name": self.c_rank_name,
            "c_rank": self.c_rank,
            "d_rank_name": self.d_rank_name,
            "d_rank": self.d_rank,
            "xiyou_seven_days_views":self.xiyou_seven_days_views,
            "xiyou_na_ratio":self.xiyou_na_ratio,
            "xiyou_ad_ratio":self.xiyou_ad_ratio,
        }

    # 搜索栏输入关键词
    def start_search(self, search_words):
        search_box = self.driver.find_element(
            By.XPATH, '//*[@id="twotabsearchtextbox"]'
        )
        search_box.send_keys(search_words)
        self.driver.find_element(By.ID, "nav-search-submit-button").click()
        logging.info(f'输入关键词{search_words}')

    def garb_search(self):
        
        self.country = 'us'
        
        # //*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]
        # //*[@id="search"]/div[2]/div[1]/div[2]/span[1]/div[1] //由于加了西柚
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="search"]/div[contains(@class,"s-desktop-content")]/div[1]/div[2]/span[1]/div[1]')
            )
        )
        div_list = self.driver.find_elements(
            By.XPATH, '//*[@id="search"]/div[2]/div[1]/div[2]/span[1]/div[1]/div'
        )
        
        logging.info(f'找到{len(div_list)}个搜索结果')

        for div in div_list:
            # 定位div的位置，方便后期调试使用
            logging.info(self.get_xpath(div))
            # 初始化单个ASIN数据单元
            self.info_init()
            # 存储所有div的class
            div_class = div.get_attribute('class')
            self.div_class_list.append(div_class)
            # 获取基本属性信息
            self.get_index(div)

            # 品牌广告
            if div_class == self.result_class_SB:
                logging.info(f'==品牌广告==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "SB"

            # 自然位置
            elif div_class == self.result_class_NR:
                logging.info(f'==自然位置==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "NR"
                self.get_search_data(div)
                # 使用default=str将所有非字符串对象转换为字符串
                logging.info(json.dumps(self.to_all_dict(), default=str))
                self.time = datetime.now().strftime("%Y-%m-%d")
                result = self.sql.replace_by_dict(
                    "asin_info_current", self.to_info_current_dict()
                )
                logging.info(f'插入数据asin_info_current:{result}')

            # 广告位置
            elif div_class == self.result_class_SP:
                logging.info(f'==广告位置==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "SP"
                self.get_search_data(div)
                logging.info(json.dumps(self.to_all_dict(), default=str))
                self.time = datetime.now().strftime("%Y-%m-%d")
                result = self.sql.replace_by_dict(
                    "asin_info_current", self.to_info_current_dict()
                )
                logging.info(f'插入数据asin_info_current:{result}')

            # 评价推荐
            elif div_class == self.result_class_HR:
                logging.info(f'==评价推荐==\t{self.data_index}=\t{self.data_cel_widget}')
                lis = div.find_elements(By.TAG_NAME, 'li')
                inner_divs = []
                for li in lis:
                    inner_divs.append(li.find_element(By.XPATH, './div'))
                for div in inner_divs:
                    # 初始化
                    self.info_init
                    self.get_index(div)
                    self.asin_all_count += 1
                    self.data_type = "HR"
                    self.get_search_data(div)
                    logging.info(json.dumps(self.to_all_dict(), default=str))
                    self.time = datetime.now().strftime("%Y-%m-%d")
                    result = self.sql.replace_by_dict(
                        "asin_info_current", self.to_info_current_dict()
                    )
                    logging.info(f'插入数据asin_info_current:{result}')

            # 视频广告
            elif div_class == self.result_class_BV:
                logging.info(f'==视频广告==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "BV"
                
            else:
                logging.info(f'=!=未知广告==\t{self.data_index}=\t{div_class}')

    # 抓取结束时统计抓取数据
    def stat_seart_result(self):
        # 去除重复元素
        self.div_class_list = DataType.remove_duplicates(self.div_class_list)
        logging.info("================")
        logging.info(self.div_class_list)
        logging.info(
            f'info_all_count: {self.info_all_count}=>info_fail_count: {self.info_fail_count}'
        )
        logging.info(
            f'asin_all_count: {self.asin_all_count}=>asin_fail_count: {self.asin_fail_count}'
        )

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
            space_interval = i*"  " 
            logging.info(f'{space_interval}{feature}')
        # 遍历当前div元素的子元素
        for child in parent.find_elements(By.XPATH, './*'):
            # 对每个子元素递归调用get_div_features()函数，获取子元素的特征
            child_feature = self.get_div_features(child, level + 1, flag)
            # 将子元素的特征添加到当前div元素的特征列表中
            feature[4].append(child_feature)
        return feature

    def cop_div_features(self, div):
        return

    # 比对div的特征值，找到配置文件中对应的section，在section中根据数据位置获取数据
    # 如果特征值在配置文件中没有找到，则保存特征值
    def match_feature_data(self, div_Info_child, config_name):
        config_file = 'yaml/features_result_'+config_name+'.yml'
        # 获取项目根目录路径
        root_folder = os.path.dirname(os.path.abspath(__file__))
        config_img = os.path.join(root_folder, 'yaml', f'img_{config_name}')
        with open(config_file) as f:
            config = yaml.safe_load(f)
        for index, child in enumerate(div_Info_child, 1):
            child_class = child.get_attribute("class")
            feature_symbol = None
            if child_class == '':
                feature_symbol = 'div'
            # logging.info(f'=={self.data_index}==')
            features_list = self.get_div_features(child, 0)
            feature_str = json.dumps(features_list)
            exists = False
            self.info_all_count += 1
            key_value = None
            value = None
            for section in config:
                if config[section]['Div_feature'] == feature_str:
                    self.count_section(section)
                    # logging.info(f'=={section}==')
                    exists = True
                    key_flag = 1
                    while key_flag > 0:
                        key_name = f'data_{key_flag}'
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
                        if data_method == 'xpath':
                            if data_type == 'hiddentext':
                                self.driver.execute_script(
                                    "arguments[0].className = '';", target_div
                                )
                            value = target_div.text
                        if data_method == 'attribute':
                            value = target_div.get_attribute(data_type)
                        logging.info(
                            f'{section}\t{self.data_index}\t{index}\t{key_value}:\n=>{value}'
                        )
                        setattr(self, data_name, value)
                        key_flag = key_flag + 1
                    break  # exists = True
            new_section = None
            if not exists:
                # 重新获取一次div特征值，并打印在文档中
                logging.info(f'==新增元素特征值：{section}\t{self.data_index}\t{index}\t{key_value}:\n=>{value}')
                self.get_div_features(child, 0, True)
                self.info_fail_count += 1
                # 'Section{}'.format(len(config)+1) len(config)+1 就是数量+1,即新增一个section后的总数，'Section{}'.format(3) = 'Section3'
                #new_section = f'{feature_symbol} data_i.{info.data_index} c.{index}'
                new_section = f'data_i.{self.data_index} c.{index}'                # 当 data_index 为 None时，该div时HR下的asin
                config[new_section] = {'Div_feature': feature_str}
                with open(config_file, 'w') as f:
                    yaml.dump(config, f)
                # 记录相关元素截图 每次运行都会造成重复运行，代码冗余。确保文件夹已创建即可
                # if not os.path.exists(config_img):
                #    os.makedirs(config_img)
                
                # 但是下面代码is_display无法正确判断元素是否可见？还是返回的内容有错误
                # 如果元素不可见。滚动页面,使元素顶部与页面顶部对齐
                #if not child.is_display():
                #    # Get the location of the seller_quickiew element
                #    x = child.location['x']
                #    y = child.location['y']
                #    # Scroll to the element's location
                #    self.driver.execute_script(f"window.scrollTo(0, {y});")
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
                #img.save(f'{config_img}\\screenshot.png')
                # 将元素顶部与页面顶部对齐后，y=0
                #logging.info(child_x, 0, child_x+child_width, child_y+child_height+20)
                img = img.crop((child_x, 0, child_x+child_width, child_height))
                img.save(f'{config_img}\\{new_section}.png')

    # 获取基本属性信息
    def get_index(self, div):
        self.asin = div.get_attribute("data-asin")
        self.data_index = div.get_attribute("data-index")
        self.data_uuid = div.get_attribute("data-uuid")
        self.data_component_type = div.get_attribute("data-component-type")
        self.data_component_id = div.get_attribute("data-component-id")
        self.data_cel_widget = div.get_attribute("data-cel-widget")

    # 获取div_info中的数据
    def get_search_data(self, div):
        # 找到 "a-section a-spacing-base" 为class的div
        # div_main = self.find_target_div_by_class(div, "a-section a-spacing-base")
        div_main = div.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base']")[0]
        # 同级div下的是卖家精灵
        div_main_sibling = div_main.find_elements(By.XPATH, "./following-sibling::div")
        div_seller = None
        div_xiyou = None
        for div in div_main_sibling:
            if div.get_attribute("class") == "xy_app":
                div_seller = div
            if div.get_attribute("class") == None:
                div_xiyou = div
        # 判断是否有Amazon'sChoice 或 Best Seller标志
        div_main_child = div_main.find_elements(By.XPATH, "./div")
        div_main_child_len = len(div_main_child)
        div_main_AB = None
        if div_main_child_len == 3:
            div_main_AB = div_main.find_element(By.XPATH, "./div[1]")
            div_main_Image = div_main.find_element(By.XPATH, "./div[2]")
            div_main_Info = div_main.find_element(By.XPATH, "./div[3]")
        if div_main_child_len == 2:
            div_main_Image = div_main.find_element(By.XPATH, "./div[1]")
            div_main_Info = div_main.find_element(By.XPATH, "./div[2]")
        # div_main_AB
        if div_main_AB:
            div_Info_AB_child = div_main_AB.find_elements(By.XPATH, "./*")
            self.match_feature_data(div_Info_AB_child, 'ab')
        # div_main_Image
        if div_main_Image:
            asin_herf = div_main_Image.find_element(By.XPATH, "./span/a").get_attribute(
                "href"
            )
            self.image = div_main_Image.find_element(
                By.XPATH, "./span/a/div/img"
            ).get_attribute("src")
        # div_main_Info
        # 获取子元素，与features.yml的class特征进行配对，并抓取数据
        if div_main_Info:
            #div_Info_child = div_main_Info.find_elements(By.XPATH, "./*")
            div_Info_child = div_main_Info.find_elements(By.XPATH, "./div")
            self.match_feature_data(div_Info_child, 'info')
            # 单独获取可售剩余数量
            self.get_left_count(div_main_Info, 'span', 'left in stock')
        # div_seller
        if div_seller:
            self.get_seller_data(div_seller)
        if div_xiyou:
            self.get_xiyou_data(div_xiyou)

    def get_seller_data(self, div_seller):
        # 获取Seller信息部分
        # 获取div_seller的outer HTML
        outer_html = div_seller.get_attribute("outerHTML")
        soup = BeautifulSoup(outer_html, "html.parser")
        # 查找包含特定文本的元素
        failure_message_element = soup.find("span", class_="loading-failed-tips")
        # 检查是否存在获取产品信息失败的文本
        if failure_message_element and "获取产品信息失败" in failure_message_element.text:
            logging.info("不进行数据抓取，因为包含获取产品信息失败的文本")
            return
        
        # find 返回的是第一个匹配的元素，如果有多个满足条件的元素，它只返回第一个。空值返回 None
        # lambda 函数定义复杂的条件，确保 class 属性的值符合预期
        # div = soup.find("div", class_=lambda value: value and ("quick-view" in value) and ("quick-view-ext" in value))
        # 直接使用字符串匹配，精确某个特定的 class 属性值，不执行 lambda 函数的复杂条件判断，可能稍微快一些
        # div = soup.find("div", class_="quick-view quick-view-ext")
        # find_all 返回的是所有匹配的元素的列表，包括所有满足条件的元素。空值返回 []
        # div = soup.find_all("div", class_="quick-view quick-view-ext")
        # 品牌
        brand_span = soup.find('span', text=re.compile('品牌'))
        if brand_span:
            self.brand = brand_span.find_next_sibling('div').text
        # 排名
        rank_elements = soup.find_all("p", class_="bsr-list-item")
        for i, rank_elem in enumerate(rank_elements):
            category = rank_elem.find('span', class_='exts-color-blue').text
            number = rank_elem.find('span', class_='rank-box').text.strip('#')
            logging.info(category, number)
            if i == 0:
                self.a_rank_name = category
                self.a_rank = number
            elif i == 1:
                self.b_rank_name = category
                self.b_rank = number
            elif i == 2:
                self.c_rank_name = category
                self.c_rank = number
            else:
                self.d_rank_name = category
                self.d_rank = number
        # 重量
        weight_grams = soup.find('span', text=re.compile('grams'))
        weight_Kilograms = soup.find('span', text=re.compile('Kilograms'))
        weight_pounds = soup.find('span', text=re.compile('pounds'))
        if weight_grams:
            weight = weight_grams.text
            weight = re.search(r'(\d+\.?\d*)', weight).group(1)
            self.weight = int(weight)
            self.weight_unit = 'grams'
        elif weight_Kilograms:
            weight = weight_Kilograms.text
            weight = re.search(r'(\d+\.?\d*)', weight).group(1)
            self.weight = int(weight * 1000)
            self.weight_unit = 'grams'
        elif weight_pounds:
            weight = weight_pounds.text
            weight = re.search(r'(\d+\.?\d*)', weight).group(1)
            self.weight = int(weight * 1000 * 2.2046)
            self.weight_unit = 'grams'
        # 尺寸
        length_cm = soup.find('span', text=re.compile('cm'))
        length_inches = soup.find('span', text=re.compile('inches'))
        if length_cm:
            length = length_cm.text
            length_list = re.findall(r'(\d+\.?\d*)', length)
            length_list = [float(i) for i in length_list]
            length_list.sort(reverse=True)
            self.length_l = length_list[0]
            self.length_w = length_list[1]
            self.length_h = length_list[2]
            self.length_unit = 'cm'
        elif length_inches:
            length = length_inches.text
            length_list = re.findall(r'(\d+\.?\d*)', length)
            length_list = [float(i) for i in length_list]
            length_list.sort(reverse=True)
            self.length_l = length_list[0] * 2.54
            self.length_w = length_list[1] * 2.54
            self.length_h = length_list[2] * 2.54
            self.length_unit = 'cm'
        # 上架时间
        date_elme = soup.find('span', text=re.compile('上架时间'))
        if date_elme:
            date_span = date_elme.find_next_sibling("span")
            date_text = date_span.text
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if date_match:
                date_str = date_match.group(1)
                self.start_sale_time = datetime.strptime(date_str, '%Y-%m-%d').date()
        # 五点描述
        # 详细信息
        
    def get_xiyou_data(self, div_seller):
        outer_html = div_seller.get_attribute("outerHTML")
        soup = BeautifulSoup(outer_html, "html.parser")
        # 提取数据
        xiyou_seven_days_views = soup.find('div', class_='num').text
        xiyou_na_ratio = soup.find('div', class_='left').text
        xiyou_ad_ratio = soup.find('div', class_='right').text
        # 格式数据
        self.xiyou_seven_days_views = int(xiyou_seven_days_views.replace(',', ''))
        self.xiyou_na_ratio = float(int(xiyou_na_ratio.rstrip('%'))/100)
        self.xiyou_ad_ratio = float(int(xiyou_ad_ratio.rstrip('%'))/100)

    def format_data(self, dict):
        price_list = ["lower_price","sale_price","rrp_price","prime_price"]
        for key in price_list:
            dict[key] = re.search(r'(\d+\.?\d*)', dict[key].replace(",",".")).group(1)
        rank_list = ["a_rank","b_rank","c_rank","d_rank"]
        for key in rank_list:
            dict[key] = dict[key].strip(',')
        if dict["rrp_type"]:
            dict["rrp_type"] = dict["rrp_type"].strip(':').strip(' ')
        if dict["start_sale_time"]:
            dict["start_sale_time"] = datetime.strptime(dict["start_sale_time"], '%Y-%m-%d')
        if dict["rating"]:
            dict["rating"]= dict["rating"].split(' out of ')[0]
    
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

    def test_class_name(self, div_main_AB, div_main_Image, div_main_Info):
        # 测试三个div的class是否正确
        AB_class = "a-section a-spacing-none puis-status-badge-container aok-relative s-grid-status-badge-container puis-expand-height"
        Image_class = "s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey"
        Info_class = (
            "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"
        )
        if div_main_AB is not None:
            div_main_AB_class = div_main_AB.get_attribute("class")
            if div_main_AB_class == AB_class:
                logging.info(f'{self.data_component_id},\tdiv_main_AB_class\t相等')
        div_main_Image_class = div_main_Image.get_attribute("class")
        if Image_class in div_main_Image_class:
            logging.info(f'{self.data_component_id},\tdiv_main_Image_class\t包含')
        div_main_Info_class = div_main_Info.get_attribute("class")
        if div_main_Info_class == Info_class:
            logging.info(f'{self.data_component_id},\tdiv_main_Info_class\t相等')

    # 单独获取剩余可售数量
    def get_left_count(self, div, tag_name, keyword):
        text = self.get_tag_text_by_keyword(div, 'span', 'left in stock')
        if text != None:
            self.left_count = re.findall(r'\d+', text)[0]
            # logging.info(f'========{self.left_count}==========')

    # 计算section出现的次数
    def count_section(self, section_name):
        '''
        if section_name in self.section_dict:
            self.section_dict[section_name] += 1
        else:
            self.section_dict[section_name] = 1
        '''
        self.section_dict = defaultdict(int)
        self.section_dict[section_name] += 1

    # 首先会检查元素是否有id，如果有id，则直接使用id作为XPath。
    # 如果没有id，脚本会遍历元素的所有父节点来构建XPath。
    def get_xpath(self, element):
        # 使用JavaScript获取元素的XPath
        script = '''
        function getElementXPath(element) {
            if (element && element.id !== '')
                return 'id("' + element.id + '")';
            else
                return _getElementXPath(element);
        };
        function _getElementXPath(element) {
            var xpath = '';
            var pos, tempitem2;
            while(element !== null) {
                pos = 0;
                tempitem2 = element;
                while(tempitem2) {
                    if (tempitem2.nodeType === 1 && tempitem2.nodeName === element.nodeName) {
                        pos += 1;
                    }
                    tempitem2 = tempitem2.previousSibling;
                }
                if (element !== null) {
                    xpath = "*[" + pos + ']' + (xpath ? '/' +  xpath : '');
                }
                element = element.parentNode;
            }
            return '/' + xpath;
        };
        return getElementXPath(arguments[0]);
        '''
        return self.driver.execute_script(script, element)


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
    # p.strip_dirs().sort_stats(-1).logging.info_stats()
