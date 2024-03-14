import os
import time
import re
import json
import yaml

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

from collections import defaultdict

from PIL import Image
from PIL import Image

from Tool.Tool_Web import *
from Tool.Tool_Data import *


class AmazonSearch:
    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait, actions: ActionChains
    ):
        self.driver, self.wait, self.actions = driver, wait, actions
        self.init_value()
        self.static_value()

    def static_value(self):
        self.country = None
        self.info_all_count = 0
        self.info_fail_count = 0
        self.asin_all_count = 0
        self.asin_fail_count = 0
        self.seller = True
        self.div_class_list = list()
        self.section_dict = {}
        
        # 品牌广告
        self.result_class_SB = (
            's-result-item s-widget s-widget-spacing-large AdHolder s-flex-full-width'
        )
        # 自然结果
        self.result_class_NR = 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'
        # 商品广告
        self.result_class_SP = 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20'
        # 高评价推荐
        self.result_class_HR = 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom sg-col-12-of-16 s-widget-spacing-large'
        # sg-col-4-of-24 sg-col-4-of-12 s-result-item sg-col-4-of-16 sg-col sg-col-4-of-20
        # 视频广告
        self.result_class_BV = 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom s-widget-spacing-small sg-col-12-of-16'
        # 搜索结果抬头标题 index =1 or 2  (index=0 品牌广告时)
        # a-section a-spacing-none s-result-item s-flex-full-width s-border-bottom-none s-widget s-widget-spacing-large

    # 调试时，每次get_Search都运行一次
    def init_value(self):
        self.asin_id = None
        self.asin = None
        self.asin_url = None
        self.image = None
        self.title = None
        self.amz_choice = None
        self.best_seller = None
        self.variant_count = None
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
        self.rating = None
        self.review = None
        self.bought = None
        self.a_rank = None  # dict value
        self.b_rank = None  # dict value

        # 长期不会更改
        self.brand = None
        self.store_name = None
        self.store_id = None
        self.use_ages = None
        self.bullet_points = None
        self.base_info = None
        self.weight = None  # list value 重量，单位
        self.measure = None  # list value 长，宽，高，单位

        # 实时变化
        self.data_index = None
        self.data_uuid = None
        self.data_component_type = None
        self.data_component_id = None
        self.data_cel_widget = None
        self.data_type = None

        self.time = None

    def find_target_div_by_class(self, div, class_name):
        if div.get_attribute('class') == class_name:
            return div
        for child in div.find_elements(By.XPATH, "./div"):
            result = self.find_target_div_by_class(child, class_name)
            if result:
                return result
        return None

    def StartSearch(self, search_words):
        search_box = self.driver.find_element(
            By.XPATH, '//*[@id="twotabsearchtextbox"]'
        )
        search_box.send_keys(search_words)
        self.driver.find_element(By.ID, "nav-search-submit-button").click()

    def get_Search(self):
        # //*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]')
            )
        )
        div_list = self.driver.find_elements(
            By.XPATH, '//*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]/div'
        )

        for div in div_list:
            # 初始化数据
            self.init_value()
            # 存储所有div的class
            div_class = div.get_attribute('class')
            self.div_class_list.append(div_class)
            # 获取基本属性信息
            self.get_index(div)

            # 品牌广告
            if div_class == self.result_class_SB:
                print(f'==品牌广告==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "SB"
                continue
            
            # 自然位置
            if div_class == self.result_class_NR:
                print(f'==自然位置==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "NR"
                self.get_left_count(div, 'span', 'left in stock')
                self.get_result(div)
                continue
            
            # 广告位置
            elif div_class == self.result_class_SP:
                print(f'==广告位置==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "SP"
                self.get_left_count(div, 'span', 'left in stock')
                self.get_result(div)
                continue
            
            # 评价推荐
            if div_class == self.result_class_HR:
                print(f'==评价推荐==\t{self.data_index}=\t{self.data_cel_widget}')
                lis = div.find_elements(By.TAG_NAME, 'li')
                inner_divs = []
                for li in lis:
                    inner_divs.append(li.find_element(By.XPATH, './div'))
                for div in inner_divs:
                    # 初始化
                    self.init_value
                    self.get_index(div)
                    self.asin_all_count += 1
                    self.data_type = "HR"
                    self.get_left_count(div, 'span', 'left in stock')
                    self.get_result(div)
                continue
            
            # 视频广告
            if div_class == self.result_class_BV:
                print(f'==视频广告==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                self.data_type = "BV"
                continue

        self.div_class_list = DataType.remove_duplicates(self.div_class_list)
        print("================")
        print(self.div_class_list)
        print(f'info_all_count: {self.info_all_count}=>info_fail_count: {self.info_fail_count}')
        print(f'asin_all_count: {self.asin_all_count}=>asin_fail_count: {self.asin_fail_count}')
        
    # 获取div的特征值
    def get_div_features(self, parent, level=0):
        tag_name = parent.tag_name
        attributes = parent.get_attribute("class")
        pre_parent = parent.find_element(By.XPATH, '..')
        elements = pre_parent.find_elements(By.TAG_NAME, parent.tag_name)
        i = 0
        if level != 0:
            for i, elem in enumerate(elements):
                if elem == parent:
                    i = i + 1
                    break
        feature = [tag_name, level, i, attributes, []]
        for child in parent.find_elements(By.XPATH, './*'):
            child_feature = self.get_div_features(child, level + 1)
            feature[4].append(child_feature)
        return feature

    def cop_div_features(self, div):
        return

    # 比对div的特征值，找到配置文件中对应的section，在section中根据数据位置获取数据
    # 如果特征值在配置文件中没有找到，则保存特征值
    def get_div_data(self, div_Info_child, config_file):
        with open(config_file) as f:
            config = yaml.safe_load(f)
        for index, child in enumerate(div_Info_child, 1):
            # print(f'=={self.data_index}==')
            features_list = self.get_div_features(child, 0)
            feature_str = json.dumps(features_list)
            exists = False
            self.info_all_count += 1
            for section in config:
                if config[section]['Div_feature'] == feature_str:
                    # print(f'=={section}==')
                    exists = True
                    key_flag = 1
                    while key_flag > 0:
                        key_name = f'data_{key_flag}'
                        if key_name not in config[section]:
                            key_flag = -1
                            continue
                        key_value = config[section][key_name]
                        data_name = key_value[0]
                        data_method = key_value[1]
                        data_xpath = key_value[2]
                        data_type = key_value[3]
                        target_div = child.find_element(By.XPATH, data_xpath)
                        if data_method == 'xpath':
                            if data_type == 'hiddentext':
                                self.driver.execute_script(
                                    "arguments[0].className = '';", target_div
                                )
                            value = target_div.text
                        if data_method == 'attribute':
                            value = target_div.get_attribute(data_type)
                        print(
                            f'{section}\t{self.data_index}\t{index}\t{key_value}:\n=>{value}'
                        )
                        setattr(self, data_name, value)
                        key_flag = key_flag + 1
                    break  # exists = True
            if not exists:
                self.info_fail_count += 1
                # 'Section{}'.format(len(config)+1) len(config)+1 就是数量+1,即新增一个section后的总数，'Section{}'.format(3) = 'Section3'
                new_section = f'data_id:{self.data_index} index:{index}'
                # 当 data_index 为 None时，该div时HR下的asin
                config[new_section] = {'Div_feature': feature_str}
                with open(config_file, 'w') as f:
                    yaml.dump(config, f)

    # 获取基本属性信息
    def get_index(self, div):
        self.asin = div.get_attribute("data-asin")
        self.data_index = div.get_attribute("data-index")
        self.data_uuid = div.get_attribute("data-uuid")
        self.data_component_type = div.get_attribute("data-component-type")
        self.data_component_id = div.get_attribute("data-component-id")
        self.data_cel_widget = div.get_attribute("data-cel-widget")

    # 获取div_info中的数据
    def get_result(self, div):
        # 找到 "a-section a-spacing-base" 为class的div
        div_main = self.find_target_div_by_class(div, "a-section a-spacing-base")
        # 同级div下的是卖家精灵
        div_seller = div_main.find_element(By.XPATH, "./following-sibling::div")
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

        '''
        # 测试三个div的class是否正确
        AB_class = "a-section a-spacing-none puis-status-badge-container aok-relative s-grid-status-badge-container puis-expand-height"
        Image_class = "s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey"
        Info_class = "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"
        if div_main_AB is not None:
            div_main_AB_class = div_main_AB.get_attribute("class")
            if div_main_AB_class == AB_class:
                print(f'{data_component_id},\tdiv_main_AB_class\t相等')
        div_main_Image_class = div_main_Image.get_attribute("class")
        if Image_class in div_main_Image_class:
            print(f'{data_component_id},\tdiv_main_Image_class\t包含')
        div_main_Info_class = div_main_Info.get_attribute("class")
        if div_main_Info_class == Info_class:
            print(f'{data_component_id},\tdiv_main_Info_class\t相等')
        '''

        asin_herf = div_main_Image.find_element(By.XPATH, "./span/a").get_attribute(
            "href"
        )
        self.image = div_main_Image.find_element(
            By.XPATH, "./span/a/div/img"
        ).get_attribute("src")

        # 获取子元素，与features.yml的class特征进行配对，并抓取数据
        div_Info_child = div_main_Info.find_elements(By.XPATH, "./div")
        self.get_div_data(div_Info_child, 'yaml/features_result_info.yml')

    def get_tag_text_by_keyword(self, div, tag_name, keyword):
        spans = div.find_elements(By.TAG_NAME, tag_name)
        for span in spans:
            text = span.text
            if keyword in text:
                return text
        return None

    def get_left_count(self, div, tag_name, keyword):
        text = self.get_tag_text_by_keyword(div, 'span', 'left in stock')
        if text != None:
            self.left_count = re.findall(r'\d+', text)[0]
            # print(f'========{self.left_count}==========')

    def count_section(self,section_name):
        '''
        if section_name in self.section_dict:
            self.section_dict[section_name] += 1
        else:
            self.section_dict[section_name] = 1
        '''
        self.section_dict = defaultdict(int)
        self.section_dict[section_name] += 1


# 测试代码
if __name__ == '__main__':
    sc = ChromeStart("Seller")
    # sc.OpenPage("https://www.amazon.com/")
    sc.BindPage("https://www.amazon.com/s?k=", "Contain")
    # driver_list = sc.GetDriver
    A = sc.GetDriver()

    driver, wait, actions = sc.GetDriver()
    # AmazonS = AmazonSearch(driver_list)
    AmazonS = AmazonSearch(driver, wait, actions)
    # AmazonS.StartSearch("remote dinosaur")
    import cProfile
    import pstats
    cProfile.run("AmazonS.get_Search()","stats.txt")
    p = pstats.Stats('stats.txt')
    p.strip_dirs().sort_stats(-1).print_stats()