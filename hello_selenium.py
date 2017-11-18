import select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4_test import BeautifulSoup
import codecs
import csv

import os
import time


class CnkiSpider:
    def __init__(self):
        print('--- 1、执行初始化的步骤：设置 chrome 补丁文件的路径 ---')
        # 设置 chrome 补丁文件的路径
        chromedriver = "/Users/liwei/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def select_fill_condition(self, driver):
        '''让驱动帮我们 1、设置搜索条件 2、点击提交按钮'''
        # 将检索条件下列列表 1 设置为"全文"
        select1 = Select(driver.find_element_by_id('txt_1_sel'))
        select1.select_by_visible_text("全文")

        # 将检索条件下列列表 2 设置为"全文"
        select2 = Select(driver.find_element_by_id('txt_2_sel'))
        select2.select_by_visible_text("全文")

        # 分别设置 3 个文本框的内容
        elem1 = driver.find_element_by_id('txt_1_value1')
        elem1.send_keys(u'品牌')
        elem2 = driver.find_element_by_id('txt_1_value2')
        elem2.send_keys(u'危机')
        elem3 = driver.find_element_by_id('txt_2_value1')
        elem3.send_keys(u'联想')

        # 将搜索按钮设置为焦点，并点击
        search_button = driver.find_element_by_id('btnSearch')
        search_button.click()

    def crawl(self, target_url):
        self.driver.get(url=target_url)
        self.select_fill_condition(self.driver)
        # 强制等待 5 秒，使得搜索结果出现
        time.sleep(5)

        # 这是通过 Chrome 的开发者工具检测到的 url，这个 url 将作为真正起始列表的 url
        # 前面的页面访问有设置 cookie 等作用
        self.driver.get(
            "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&dbPrefix=CCND&dbCatalog=%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E6%8A%A5%E7%BA%B8%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93&ConfigFile=CCND.xml&research=off&t=1510819472144&keyValue=%E5%93%81%E7%89%8C&S=1")
        self.parse_content_url(self.driver.page_source)

        self.driver.close()

    def parse_content_url(self, page_source):
        '''将网页中的 url 和标题解析出来，并写入 csv 文件中'''
        # "lxml" 必须指定
        soup = BeautifulSoup(page_source, "lxml")
        url_titles = soup.select('a[class="fz14"]')
        with open('urls.csv', 'a', encoding='utf-8') as fw:
            writer = csv.writer(fw)
            for index, item in enumerate(url_titles):
                # print(index, self.handle_url(item['href']), item.text)
                writer.writerow(list((str(index), self.handle_url(item['href']), item.text)))

    def handle_url(self, url):
        new_str = url[4:]
        return "http://kns.cnki.net/KCMS" + new_str


if __name__ == '__main__':
    cnkiSpider = CnkiSpider()
    target_url = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CCND'
    cnkiSpider.crawl(target_url)
