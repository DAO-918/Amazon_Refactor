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

from PIL import Image
from PIL import Image

from Tool.Tool_Web import *
from Tool.Tool_Data import *


class AmazonSearch:
    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait, actions: ActionChains
    ):
        self.driver, self.wait, self.actions = driver, wait, actions
        self.init_value
        
    def static_value(self):
        self.country = None

    # 调试时，每次get_Search都运行一次
    def init_value(self):
        self.asin = None
        self.asin_url = None
        self.image = None
        self.title = None
        self.amz_choice = None
        self.best_seller = None
        self.variant_count = None
        self.is_deal = None # boolean value
        self.fba = None
        self.is_fba = None # boolean value
        self.is_amz = None # boolean value
        self.is_smb = None # boolean value
        self.lower_price = None
        self.lower_list = None
        self.lowest_precent = None
        self.sale_price = None
        self.rrp_price = None
        self.rrp_type = None
        self.prime_price = None
        self.discount = None
        self.coupon  = None
        self.saving  = None
        self.promotion  = None
        self.rating  = None
        self.review  = None
        self.bought = None
        self.a_rank = None # dict value
        self.b_rank = None # dict value
        self.brand  = None
        self.store_name = None
        self.store_id = None
        self.use_ages = None
        self.bullet_points = None
        self.base_info = None
        self.weight= None # list value 重量，单位
        self.measure = None # list value 长，宽，高，单位

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
        config_file = 'features.yml'
        with open(config_file) as f:
            config = yaml.safe_load(f)
        # //*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]')
            )
        )
        div_list = self.driver.find_elements(
            By.XPATH, '//*[@id="search"]/div[1]/div[1]/div[2]/span[1]/div[1]/div'
        )
        div_class_list = list()
        for div in div_list:
            div_class = div.get_attribute('class')
            print(div.__class__)
            print(div_class)
            div_class_list.append(div_class)
            # 品牌广告
            # s-result-item s-widget s-widget-spacing-large AdHolder s-flex-full-width
            if (
                div_class
                == "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"
            ):
                print("品牌广告")
            # 自然结果
            # sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20
            if (
                div_class
                == "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"
            ):
                print("自然结果")
                data_asin = div.get_attribute("data-asin")
                data_index = div.get_attribute("data-index")
                data_uuid = div.get_attribute("data-uuid")
                data_component_type = div.get_attribute("data-component-type")
                data_component_id = div.get_attribute("data-component-id")
                data_cel_widget = div.get_attribute("data-cel-widget")
                div_main = self.find_target_div_by_class(
                    div, "a-section a-spacing-base"
                )
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
                # a-section a-spacing-none puis-status-badge-container aok-relative s-grid-status-badge-container puis-expand-height
                # s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey s-padding-left-small s-padding-right-small puis-spacing-small s-height-equalized puis puis-v1g4cn23aiw4pq21ytu1qia8qu3
                # a-section a-spacing-small puis-padding-left-small puis-padding-right-small
                AB_class = "a-section a-spacing-none puis-status-badge-container aok-relative s-grid-status-badge-container puis-expand-height"
                if div_main_AB is not None:
                    div_main_AB_class = div_main_AB.get_attribute("class")
                    if div_main_AB_class == AB_class:
                        print(f'{data_component_id},\tdiv_main_AB_class\t相等')
                Image_class = "s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey"
                div_main_Image_class = div_main_Image.get_attribute("class")
                if Image_class in div_main_Image_class:
                    print(f'{data_component_id},\tdiv_main_Image_class\t包含')
                Info_class = "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"
                div_main_Info_class = div_main_Info.get_attribute("class")
                if div_main_Info_class == Info_class:
                    print(f'{data_component_id},\tdiv_main_Info_class\t相等')

                asin_herf = div_main_Image.find_element(
                    By.XPATH, "./span/a"
                ).get_attribute("href")
                asin_image = div_main_Image.find_element(
                    By.XPATH, "./span/a/div/img"
                ).get_attribute("src")

                div_Info_child = div_main_Info.find_elements(By.XPATH, "./div")
                
                
                '''for index,child in enumerate(div_Info_child,1):
                    print(child.__class__)
                    features_list = self.get_div_features(child, 0)
                    print(features_list)
                    feature_str = json.dumps(features_list)
                    exists = False
                    for section in config:
                        print(section)
                        print(config[section])
                        print(config[section]['Div_feature'])
                        if config[section]['Div_feature'] == feature_str:
                            exists = True
                            break
                    if not exists:
                        # 'Section{}'.format(len(config)+1) len(config)+1 就是数量+1,即新增一个section后的总数，'Section{}'.format(3) = 'Section3'
                        new_section = f'data_id:{data_index} index:{index}'
                        config[new_section] = {'Div_feature': feature_str}

                with open(config_file, 'w') as f:
                    yaml.dump(config, f)'''
                
                
                for index,child in enumerate(div_Info_child,1):
                    print(child.__class__)
                    features_list = self.get_div_features(child, 0)
                    print(features_list)
                    feature_str = json.dumps(features_list)
                    exists = False
                    for section in config:
                        if config[section]['Div_feature'] == feature_str:
                            print(section)
                            exists = True
                            key_flag = 1
                            while key_flag > 0 :
                                key_name = f'data_{key_flag}'
                                if key_name not in config[section]:
                                    key_flag = -1
                                    continue
                                key_value = config[section][key_name]
                                data_name = key_value[0]
                                data_method = key_value[1]
                                data_xpath = key_value[2]
                                data_type = key_value[3]
                                print(key_value)
                                target_div = child.find_element(By.XPATH, data_xpath)
                                if data_method == 'xpath':
                                    if data_type == 'hiddentext':
                                        print(self.driver.__class__)
                                        self.driver.execute_script("arguments[0].className = '';", target_div)
                                    value = target_div.text
                                if data_method == 'attribute':
                                    value = target_div.get_attribute(data_type)
                                print(value)
                                setattr(self,data_name,value)
                                key_flag = key_flag+1
                            break # exists = True
                    if not exists:
                        # 'Section{}'.format(len(config)+1) len(config)+1 就是数量+1,即新增一个section后的总数，'Section{}'.format(3) = 'Section3'
                        new_section = f'data_id:{data_index} index:{index}'
                        config[new_section] = {'Div_feature': feature_str}
                        with open(config_file, 'w') as f:
                            yaml.dump(config, f)
                
                # 多变体
                # a-section a-spacing-small puis-padding-left-small puis-padding-right-small
                # a-section a-spacing-none a-text-center

                # 标题
                # a-section a-spacing-none a-spacing-top-small s-title-instructions-style
                # a-size-mini a-spacing-none a-color-base s-line-clamp-4
                #asin_title = (
                #    div_Info_child[0].find_element(By.XPATH, "./h2/a/span").text()
                #)

                # 评分
                # a-section a-spacing-none a-spacing-top-micro
                # a-row a-size-small
                # a-row a-size-base
                #asin_ratings = (
                #    div_Info_child[0]
                #    .find_element(By.XPATH, "./div[1]/span[1]")
                #    .get_attribute("aria-label")
                #)
                #asin_score = (
                #    div_Info_child[0]
                #    .find_element(By.XPATH, "./div[1]/span[1]/span")
                #    .text()
                #)
                #asin_bought = (
                #    div_Info_child[0].find_element(By.XPATH, "./div[2]/span").text()
                #)

                # 价格
                # a-section a-spacing-none a-spacing-top-small s-price-instructions-style
                # a-row 秒杀时
                # a-row a-size-base a-color-base
                # a-row a-size-base a-color-secondary
                #asin_Deal = (
                #    div_Info_child[0]
                #    .find_element(By.XPATH, "./div[1]/a/span/span/span/span")
                #    .text()
                #)
                # 有RRP时
                #asin_price = div_Info_child[0].find_element(
                #    By.XPATH, "./div[2]/a/span/span[1]"
                #)  # 需要取消隐藏
                #asin_RRP_type = (
                #    div_Info_child[0]
                #    .find_element(By.XPATH, "./div[2]/a/div/span[1]")
                #    .text()
                #)
                # <span class="a-offscreen">$35.99</span> <span aria-hidden="true">$35.99</span>
                #asin_RRP = div_Info_child[0].find_element(
                #    By.XPATH, "./div[2]/a/div/span[2]/span[1]"
                #)  # 需要取消隐藏
                #asin_coupon = (
                #    div_Info_child[0]
                #    .find_element(By.XPATH, "./span/span[2]/span[1]")
                #    .text()
                #)
                #div_Info_child[0].get_dom_attribute

                # 配送
                # a-section a-spacing-none a-spacing-top-micro
                # a-row a-size-base a-color-secondary s-align-children-center

                # 商店
                # a-section a-spacing-none a-spacing-top-micro
                # a-section a-spacing-none s-align-children-center
                # a-popover-preload  //  id="a-popover-pc-popover-B08J1M8XJB"

                # 年龄
                # a-section a-spacing-none a-spacing-top-mini
                # a-row a-size-base a-color-base
                #asin_age = div_Info_child[0].find_element(By.XPATH, "./div/span").text()

                # 匹配结果可能有两个，自然+广告
                # B09V38ST65-amazons-choice-supplementary
                # B09PVKBP61-best-seller-supplementary

            # SD广告
            # sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20
            # Highly rated
            # sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom sg-col-12-of-16 s-widget-spacing-large
            # 视频广告
            # sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col s-flex-geom s-widget-spacing-small sg-col-12-of-16
            # 自然结果 - More results
            # sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20
            # 没有显示
            # sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20

        #div_class_list = DataType.remove_duplicates(div_class_list)
        #print(div_class_list)

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
    AmazonS.get_Search()
