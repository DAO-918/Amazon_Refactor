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


class AmazonDeal:
    def __init__(
        self, driver: webdriver.Chrome, wait: WebDriverWait, actions: ActionChains
    ):
        self.driver, self.wait, self.actions = driver, wait, actions
        self.static_value()

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

    # 调试时，每次get_Search都运行一次
    def info_init(info):
        info.asin = None
        info.time = None
        info.image = None
        info.title = None
        info.deal_relate  = None
        info.data_deal_id = None
        info.data_csa_c_id = None
        info.off_discount  = None
        info.off_price  = None
        info.claimed  = None
        info.start_time  = None
        info.page_count  = None
        info.locate_count  = None
        info.index_count  = None
        return info

    def select_deal_tag(self,deal_tag_name):
        toy_select_parent = self.driver.find_element(By.XPATH,'//*[@id="grid-main-container"]/div[2]')
        toy_select_spans = toy_select_parent.find_element(By.XPATH,f'.//span[text()="{deal_tag_name}"]')
        # sibling：当前元素节点的同级节点，结合preceding，following使用
        # preceding-sibling：当前元素节点之前的同级节点
        # following-sibling：当前元素节点之后的同级节点
        toy_select_input = toy_select_spans.find_element(By.XPATH,'./preceding-sibling::input')
        toy_select_input.click()
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

    def garb_deal(self,info):
            while True:
                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[@id='grid-main-container']/div[3]/div")
                    )
                )
                time.sleep(10)
                
                div = self.driver.find_element(By.XPATH, '//*[@id="dealsGridLinkAnchor"]')
                div_next_page = div.find_element(By.XPATH, '//div[contains(@class, "GridContainer-module__gridFooter")]')
                outer_html = div_next_page.get_attribute("outerHTML")
                soup = BeautifulSoup(outer_html, "html.parser")
                # 找到当前页码元素
                curr_li = soup.find('li', class_='a-selected')
                # 下一个页码li
                # curr_li.find_next_sibling('li').click()
                curr_page = int(curr_li.text)

                # 找到总页数 
                # last_li = soup.find('li', class_=lambda value: value and ("a-last" in value))
                last_li = soup.select('li.a-last')[-1]
                total_page = int(last_li.text)

                # 如果不是最后一页,点击下一页
                if curr_page < total_page:
                    soup.find('li', class_='a-last').click()
                    last_li_element = self.driver.find_element(By.XPATH,last_li.prettify())
                    last_li_element.click()
                # 获取页码
                page_index = int(
                    self.driver.find_element(
                        By.XPATH,
                        '//*[@id="dealsGridLinkAnchor"]/div/div[3]/div/ul/li[@class="a-selected"]/a',
                    ).text
                )
                # 是否是最后一页
                page_next = driver.find_element(
                    By.XPATH,
                    '//*[@id="dealsGridLinkAnchor"]/div/div[3]/div/ul/li[contains(@class, "a-last")]',
                )
                isLastPage = False
                if "a-disabled" in page_next.get_attribute("class"):  # type: ignore
                    isLastPage = True

                parent = driver.find_element(
                    By.XPATH, '//*[@id="grid-main-container"]/div[3]/div'
                )
                divs = parent.find_elements(By.XPATH, './div')

                for located, div in enumerate(divs, start=1):
                    try:
                        position = (page_index - 1) * 60 + int(located)
                        # 获取LINK ASIN //*[@id="grid-main-container"]/div[3]/div/div[57] /div/div/a
                        #               //*[@id="grid-main-container"]/div[3]/div/div[1]
                        link = div.find_element(By.XPATH, './div/div/a').get_attribute('href')
                        if '/deal' in link or '/dp/' not in link:  # type: ignore
                            div_inner = div.find_element(By.XPATH, './div/div/a/div/div/img')
                            img_url = div_inner.get_attribute('data-a-hires')  # 或 src
                            title = div_inner.get_attribute('alt')
                            topic_deal.append((link, img_url, title, page_index, located, position))  # type: ignore
                            data.append(
                                (
                                    link,
                                    None,
                                    None,
                                    img_url,
                                    title,
                                    None,
                                    None,
                                    page_index,
                                    located,
                                    position,
                                    datetime.datetime.now().strftime("%Y%m%d-%H:%M"),
                                    True,
                                    '',
                                    0,
                                    0,
                                )
                            )
                            continue

                        link_dict = regex_ASIN(link)
                        link = regex_Link(link_dict["ASIN"], link_dict["国家"])["链接"]
                        # 获取图片地址 //*[@id="grid-main-container"]/div[3]/div/div[3] /div/div/a/div/div/img
                        div_inner = div.find_element(By.XPATH, './div/div/a/div/div/img')
                        img_url = div_inner.get_attribute('data-a-hires')  # 或 src
                        # 获取标题
                        title = div_inner.get_attribute('alt')
                        # 获取Deal折扣
                        discount = div.find_element(
                            By.XPATH, './div/div/div/span/div[1]/div'
                        ).text.replace(' off', '')
                        # 获取claimed进度
                        claimed = None
                        try:
                            claimed = div.find_element(
                                By.XPATH, './div/div/div/div/span/div/div[2]/span/div'
                            ).text.replace(' claimed', '')
                        except Exception:
                            print('Not Found Claimed Bar')

                        if int(page_index) == 1 and int(located) == 9:
                            global_contry = link_dict["国家"]
                            global_link_f = link[:-10]

                        # columns=['Link','ASIN','Country','Image URL','Title', 'Discount', 'Claimed','Page','Located','Position','Time','IsTop']
                        data.append(
                            (
                                link,
                                link_dict["ASIN"],
                                link_dict["国家"],
                                img_url,
                                title,
                                discount,
                                claimed,
                                page_index,
                                located,
                                position,
                                datetime.datetime.now().strftime("%Y%m%d-%H:%M"),
                                False,
                                '',
                                0,
                                0,
                            )
                        )
                        print(
                            f'第{page_index}页:\t第{located}个:\t{link_dict["ASIN"]}\t{discount}\t{claimed}'
                        )
                    except Exception as e:
                        print('抓取错误')

                if isLastPage:
                    break

                page_next.click()

    
# 测试代码
if __name__ == '__main__':
    # us
    deal_us_url = "https://www.amazon.com/events/deals"
    # uk
    deal_uk_url = "https://www.amazon.co.uk/gp/goldbox"
    
    sc = ChromeStart("Seller", 9222)
    # sc.OpenPage("https://www.amazon.com/")
    sc.BindPage(deal_us_url, "Contain")
    driver, wait, actions = sc.GetDriver()
    AmazonS = AmazonDeal(driver, wait, actions)
    AmazonS.select_deal_tag("Toys & Games")
    