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
    
    # 默认值
    def static_value(self):
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
    def info_init(info):
        info.asin = None
        info.asin_url = None  # 点击后跳转的url链接？
        info.image = None
        info.title = None
        info.amz_choice = None
        info.best_seller = None
        info.variant = None
        info.variant_type = None
        info.variant_count = None
        info.deal_type = None
        info.is_deal = None  # boolean value
        info.fba = None
        info.is_fba = None  # boolean value
        info.is_amz = None  # boolean value
        info.is_smb = None  # boolean value
        info.left_count = None  # TINYINT
        info.lower_price = None
        info.lower_list = None
        info.lowest_precent = None
        info.sale_price = None
        info.rrp_price = None
        info.rrp_type = None
        info.prime_price = None
        info.discount = None
        info.coupon = None
        info.saving = None
        info.promotion = None
        info.promotion_code = None
        info.rating = None
        info.review = None
        info.bought = None
        info.a_rank_name = None
        info.a_rank = None
        info.b_rank_name = None
        info.b_rank = None
        info.c_rank_name = None
        info.c_rank = None
        info.d_rank_name = None
        info.d_rank = None

        # 长期不会更改
        info.brand = None
        info.merchant_token = None
        info.use_age = None
        info.use_ages_do = None
        info.use_ages_up = None
        info.bullet_points_1 = None
        info.bullet_points_2 = None
        info.bullet_points_3 = None
        info.bullet_points_4 = None
        info.bullet_points_5 = None
        info.bullet_points_6 = None
        info.bullet_points = None
        info.base_info = None
        info.weight = None
        info.weight_unit = None
        info.length_l = None
        info.length_w = None
        info.length_h = None
        info.length_unit = None
        info.start_sale_time = None
        
        # 西柚数据
        info.xiyou_seven_days_views =None
        info.xiyou_na_ratio = None
        info.xiyou_ad_ratio = None

        # 实时变化
        info.data_index = None
        info.data_uuid = None
        info.data_component_type = None
        info.data_component_id = None
        info.data_cel_widget = None
        info.data_type = None

        info.time = None

        return info

    def to_all_dict(self, info):
        return {
            "asin": info.asin,
            "asin_url": info.asin_url,
            "image": info.image,
            "title": info.title,
            "amz_choice": info.amz_choice,
            "best_seller": info.best_seller,
            "variant": info.variant,
            "variant_type": info.variant_type,
            "variant_count": info.variant_count,
            "deal_type": info.deal_type,
            "is_deal": info.is_deal,
            "fba": info.fba,
            "is_fba": info.is_fba,
            "is_amz": info.is_amz,
            "is_smb": info.is_smb,
            "left_count": info.left_count,
            "lower_price": info.lower_price,
            "lower_list": info.lower_list,
            "lowest_precent": info.lowest_precent,
            "sale_price": info.sale_price,
            "rrp_price": info.rrp_price,
            "rrp_type": info.rrp_type,
            "prime_price": info.prime_price,
            "discount": info.discount,
            "coupon": info.coupon,
            "saving": info.saving,
            "promotion": info.promotion,
            "rating": info.rating,
            "review": info.review,
            "bought": info.bought,
            "a_rank_name": info.a_rank_name,
            "a_rank": info.a_rank,
            "b_rank_name": info.b_rank_name,
            "b_rank": info.b_rank,
            "c_rank_name": info.c_rank_name,
            "c_rank": info.c_rank,
            "d_rank_name": info.d_rank_name,
            "d_rank": info.d_rank,
            "brand": info.brand,
            "merchant_token": info.merchant_token,
            "use_age": info.use_age,
            "use_ages_do": info.use_ages_do,
            "use_ages_up": info.use_ages_up,
            "bullet_points_1": info.bullet_points_1,
            "bullet_points_2": info.bullet_points_2,
            "bullet_points_3": info.bullet_points_3,
            "bullet_points_4": info.bullet_points_4,
            "bullet_points_5": info.bullet_points_5,
            "bullet_points_6": info.bullet_points_6,
            "bullet_points": info.bullet_points,
            "base_info": info.base_info,
            "weight": info.weight,
            "weight_unit": info.weight_unit,
            "length_l": info.length_l,
            "length_w": info.length_w,
            "length_h": info.length_h,
            "length_unit": info.length_unit,
            "start_sale_time": info.start_sale_time,
            "data_index": info.data_index,
            "data_uuid": info.data_uuid,
            "data_component_type": info.data_component_type,
            "data_component_id": info.data_component_id,
            "data_cel_widget": info.data_cel_widget,
            "data_type": info.data_type,
            "xiyou_seven_days_views":info.xiyou_seven_days_views,
            "xiyou_na_ratio":info.xiyou_na_ratio,
            "xiyou_ad_ratio":info.xiyou_ad_ratio,
            "time": info.time
        }

    def to_info_current_dict(self, info):
        return {
            "asin": info.asin,
            "country": self.country,
            "time": info.time,
            "image": info.image,
            "title": info.title,
            "brand": info.brand,
            "merchant_token": info.merchant_token,
            "amz_choice": info.amz_choice,
            "best_seller": info.best_seller,
            "deal_type": info.deal_type,
            "is_deal": info.is_deal,
            "is_fba": info.is_fba,
            "is_amz": info.is_amz,
            "is_smb": info.is_smb,
            "left_count": info.left_count,
            "lower_price": info.lower_price,
            "lower_list": info.lower_list,
            "lowest_precent": info.lowest_precent,
            "sale_price": info.sale_price,
            "rrp_price": info.rrp_price,
            "rrp_type": info.rrp_type,
            "prime_price": info.prime_price,
            "discount": info.discount,
            "coupon": info.coupon,
            "saving": info.saving,
            "promotion": info.promotion,
            "promotion_code": info.promotion_code,
            "rating": info.rating,
            "review": info.review,
            "bought": info.bought,
            "a_rank_name": info.a_rank_name,
            "a_rank": info.a_rank,
            "b_rank_name": info.b_rank_name,
            "b_rank": info.b_rank,
            "c_rank_name": info.c_rank_name,
            "c_rank": info.c_rank,
            "d_rank_name": info.d_rank_name,
            "d_rank": info.d_rank,
            "xiyou_seven_days_views":info.xiyou_seven_days_views,
            "xiyou_na_ratio":info.xiyou_na_ratio,
            "xiyou_ad_ratio":info.xiyou_ad_ratio,
        }

    def start_search(self, search_words):
        search_box = self.driver.find_element(
            By.XPATH, '//*[@id="twotabsearchtextbox"]'
        )
        search_box.send_keys(search_words)
        self.driver.find_element(By.ID, "nav-search-submit-button").click()

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

        for div in div_list:
            # 初始化数据
            info = self.info_init()
            # 存储所有div的class
            div_class = div.get_attribute('class')
            self.div_class_list.append(div_class)
            # 获取基本属性信息
            self.get_index(info, div)

            # 品牌广告
            if div_class == self.result_class_SB:
                print(f'==品牌广告==\t{self.data_index}=\t{self.data_cel_widget}')
                self.asin_all_count += 1
                info.data_type = "SB"
                continue

            # 自然位置
            if div_class == self.result_class_NR:
                print(f'==自然位置==\t{info.data_index}=\t{info.data_cel_widget}')
                self.asin_all_count += 1
                info.data_type = "NR"
                self.get_search_data(info, div)
                # 使用default=str将所有非字符串对象转换为字符串
                print(json.dumps(self.to_all_dict(info), default=str))
                info.time = datetime.now().strftime("%Y-%m-%d")
                result = self.sql.replace_by_dict(
                    "asin_info_current", self.to_info_current_dict(info)
                )
                print(f'插入数据asin_info_current:{result}')
                continue

            # 广告位置
            elif div_class == self.result_class_SP:
                print(f'==广告位置==\t{info.data_index}=\t{info.data_cel_widget}')
                self.asin_all_count += 1
                info.data_type = "SP"
                self.get_search_data(info, div)
                print(json.dumps(self.to_all_dict(info), default=str))
                info.time = datetime.now().strftime("%Y-%m-%d")
                result = self.sql.replace_by_dict(
                    "asin_info_current", self.to_info_current_dict(info)
                )
                print(f'插入数据asin_info_current:{result}')
                continue

            # 评价推荐
            if div_class == self.result_class_HR:
                print(f'==评价推荐==\t{info.data_index}=\t{info.data_cel_widget}')
                lis = div.find_elements(By.TAG_NAME, 'li')
                inner_divs = []
                for li in lis:
                    inner_divs.append(li.find_element(By.XPATH, './div'))
                for div in inner_divs:
                    # 初始化
                    self.info_init
                    self.get_index(info, div)
                    self.asin_all_count += 1
                    info.data_type = "HR"
                    self.get_search_data(info, div)
                    print(json.dumps(self.to_all_dict(info), default=str))
                    info.time = datetime.now().strftime("%Y-%m-%d")
                    result = self.sql.replace_by_dict(
                        "asin_info_current", self.to_info_current_dict(info)
                    )
                    print(f'插入数据asin_info_current:{result}')
                continue

            # 视频广告
            if div_class == self.result_class_BV:
                print(f'==视频广告==\t{info.data_index}=\t{info.data_cel_widget}')
                self.asin_all_count += 1
                info.data_type = "BV"
                continue

        self.div_class_list = DataType.remove_duplicates(self.div_class_list)
        print("================")
        print(self.div_class_list)
        print(
            f'info_all_count: {self.info_all_count}=>info_fail_count: {self.info_fail_count}'
        )
        print(
            f'asin_all_count: {self.asin_all_count}=>asin_fail_count: {self.asin_fail_count}'
        )

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
    def match_feature_data(self, info, div_Info_child, config_name):
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
            # print(f'=={self.data_index}==')
            features_list = self.get_div_features(child, 0)
            feature_str = json.dumps(features_list)
            exists = False
            self.info_all_count += 1
            for section in config:
                if config[section]['Div_feature'] == feature_str:
                    self.count_section(section)
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
                            f'{section}\t{info.data_index}\t{index}\t{key_value}:\n=>{value}'
                        )
                        setattr(info, data_name, value)
                        key_flag = key_flag + 1
                    break  # exists = True
                
            new_section = None
            if not exists:
                self.info_fail_count += 1
                # 'Section{}'.format(len(config)+1) len(config)+1 就是数量+1,即新增一个section后的总数，'Section{}'.format(3) = 'Section3'
                #new_section = f'{feature_symbol} data_i.{info.data_index} c.{index}'
                new_section = f'data_i.{info.data_index} c.{index}'

                # 当 data_index 为 None时，该div时HR下的asin
                config[new_section] = {'Div_feature': feature_str}
                with open(config_file, 'w') as f:
                    yaml.dump(config, f)
                
                # 记录相关元素截图
                if not os.path.exists(config_img):
                    os.makedirs(config_img)
                # 如果元素不可见。滚动页面,使元素顶部与页面顶部对齐
                #if not child.isd():
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
                #print(child_x, 0, child_x+child_width, child_y+child_height+20)
                img = img.crop((child_x, 0, child_x+child_width, child_height))
                img.save(f'{config_img}\\{new_section}.png')

    # 获取基本属性信息
    def get_index(self, info, div):
        info.asin = div.get_attribute("data-asin")
        info.data_index = div.get_attribute("data-index")
        info.data_uuid = div.get_attribute("data-uuid")
        info.data_component_type = div.get_attribute("data-component-type")
        info.data_component_id = div.get_attribute("data-component-id")
        info.data_cel_widget = div.get_attribute("data-cel-widget")

    # 获取div_info中的数据
    def get_search_data(self, info, div):
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
            self.match_feature_data(info, div_Info_AB_child, 'ab')
        # div_main_Image
        if div_main_Image:
            asin_herf = div_main_Image.find_element(By.XPATH, "./span/a").get_attribute(
                "href"
            )
            info.image = div_main_Image.find_element(
                By.XPATH, "./span/a/div/img"
            ).get_attribute("src")
        # div_main_Info
        # 获取子元素，与features.yml的class特征进行配对，并抓取数据
        if div_main_Info:
            div_Info_child = div_main_Info.find_elements(By.XPATH, "./div")
            self.match_feature_data(info, div_Info_child, 'info')
            # 单独获取可售剩余数量
            self.get_left_count(info, div_main_Info, 'span', 'left in stock')
        # div_seller
        if div_seller:
            self.get_seller_data(info, div_seller)
        if div_xiyou:
            self.get_xiyou_data(info, div_xiyou)

    def get_seller_data(self, info, div_seller):
        # 获取Seller信息部分
        # 获取div_seller的outer HTML
        outer_html = div_seller.get_attribute("outerHTML")
        soup = BeautifulSoup(outer_html, "html.parser")
        # 查找包含特定文本的元素
        failure_message_element = soup.find("span", class_="loading-failed-tips")
        # 检查是否存在获取产品信息失败的文本
        if failure_message_element and "获取产品信息失败" in failure_message_element.text:
            print("不进行数据抓取，因为包含获取产品信息失败的文本")
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
            info.brand = brand_span.find_next_sibling('div').text
        # 排名
        rank_elements = soup.find_all("p", class_="bsr-list-item")
        for i, rank_elem in enumerate(rank_elements):
            category = rank_elem.find('span', class_='exts-color-blue').text
            number = rank_elem.find('span', class_='rank-box').text.strip('#')
            print(category, number)
            if i == 0:
                info.a_rank_name = category
                info.a_rank = number
            elif i == 1:
                info.b_rank_name = category
                info.b_rank = number
            elif i == 2:
                info.c_rank_name = category
                info.c_rank = number
            else:
                info.d_rank_name = category
                info.d_rank = number
        # 重量
        weight_grams = soup.find('span', text=re.compile('grams'))
        weight_Kilograms = soup.find('span', text=re.compile('Kilograms'))
        weight_pounds = soup.find('span', text=re.compile('pounds'))
        if weight_grams:
            weight = weight_grams.text
            weight = re.search(r'(\d+\.?\d*)', weight).group(1)
            info.weight = int(weight)
            info.weight_unit = 'grams'
        elif weight_Kilograms:
            weight = weight_Kilograms.text
            weight = re.search(r'(\d+\.?\d*)', weight).group(1)
            info.weight = int(weight * 1000)
            info.weight_unit = 'grams'
        elif weight_pounds:
            weight = weight_pounds.text
            weight = re.search(r'(\d+\.?\d*)', weight).group(1)
            info.weight = int(weight * 1000 * 2.2046)
            info.weight_unit = 'grams'
        # 尺寸
        length_cm = soup.find('span', text=re.compile('cm'))
        length_inches = soup.find('span', text=re.compile('inches'))
        if length_cm:
            length = length_cm.text
            length_list = re.findall(r'(\d+\.?\d*)', length)
            length_list = [float(i) for i in length_list]
            length_list.sort(reverse=True)
            info.length_l = length_list[0]
            info.length_w = length_list[1]
            info.length_h = length_list[2]
            info.length_unit = 'cm'
        elif length_inches:
            length = length_inches.text
            length_list = re.findall(r'(\d+\.?\d*)', length)
            length_list = [float(i) for i in length_list]
            length_list.sort(reverse=True)
            info.length_l = length_list[0] * 2.54
            info.length_w = length_list[1] * 2.54
            info.length_h = length_list[2] * 2.54
            info.length_unit = 'cm'
        # 上架时间
        date_elme = soup.find('span', text=re.compile('上架时间'))
        if date_elme:
            date_span = date_elme.find_next_sibling("span")
            date_text = date_span.text
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if date_match:
                date_str = date_match.group(1)
                info.start_sale_time = datetime.strptime(date_str, '%Y-%m-%d').date()
        # 五点描述
        # 详细信息
        
    def get_xiyou_data(self, info, div_seller):
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

    def test_class_name(info, div_main_AB, div_main_Image, div_main_Info):
        # 测试三个div的class是否正确
        AB_class = "a-section a-spacing-none puis-status-badge-container aok-relative s-grid-status-badge-container puis-expand-height"
        Image_class = "s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey"
        Info_class = (
            "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"
        )
        if div_main_AB is not None:
            div_main_AB_class = div_main_AB.get_attribute("class")
            if div_main_AB_class == AB_class:
                print(f'{info.data_component_id},\tdiv_main_AB_class\t相等')
        div_main_Image_class = div_main_Image.get_attribute("class")
        if Image_class in div_main_Image_class:
            print(f'{info.data_component_id},\tdiv_main_Image_class\t包含')
        div_main_Info_class = div_main_Info.get_attribute("class")
        if div_main_Info_class == Info_class:
            print(f'{info.data_component_id},\tdiv_main_Info_class\t相等')

    # 单独获取剩余可售数量
    def get_left_count(self, info, div, tag_name, keyword):
        text = self.get_tag_text_by_keyword(div, 'span', 'left in stock')
        if text != None:
            info.left_count = re.findall(r'\d+', text)[0]
            # print(f'========{self.left_count}==========')

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
    # p.strip_dirs().sort_stats(-1).print_stats()
