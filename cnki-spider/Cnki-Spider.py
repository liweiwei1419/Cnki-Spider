import select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import csv

import os
import time


class CnkiSpider:
    def __init__(self):
        print('--- 1、执行初始化的步骤：设置 chrome 补丁文件的路径 ---')
        # 设置 chrome 补丁文件的路径
        # self.driver = webdriver.Chrome(executable_path='/Users/liwei/chromedriver')
        self.driver = webdriver.Firefox(executable_path="/Users/liwei/geckodriver")

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

    def parse_content_url(self, page_source):
        '''将网页中的序号、 url 和标题解析出来，并写入 csv 文件中'''
        # "lxml" 必须指定，这是官方推荐的解释器
        soup = BeautifulSoup(page_source, "lxml")
        with open('test.html', 'w', encoding='utf-8') as fw:
            fw.write(page_source)

        rows = soup.select('.GridTableContent tr')[1:]
        with open('urls.csv', 'a', encoding='utf-8') as fw:
            writer = csv.writer(fw)
            for row in rows:
                order_number = row.select('td')[0].text
                href = row.select('a')[0].get('href')
                title = row.select('a')[0].text
                writer.writerow(list((order_number, self.handle_url(href), title)))

    def handle_url(self, url):
        new_str = url[4:]
        return "http://kns.cnki.net/KCMS" + new_str

    def crawl_next_page(self, content):
        '''
        首先判断是否有下一页按钮，
        如果有下一页按钮就点击它，继续爬取论文列表；
        如果没有，就停止爬虫
        :param content:
        :return:
        '''
        soup = BeautifulSoup(content, 'lxml')
        # 所有 a 标签的集合
        a_list = soup.select('div.TitleLeftCell a')
        if a_list:
            next_link = a_list[-1]
            if next_link.get_text() == '下一页':
                print("有下一页按钮")
                # 注意：要将页面定位到页面底端，Selenium 才会帮我们点击按钮
                # 点击下一页按钮
                next_link = self.driver.find_element_by_css_selector('div.TitleLeftCell a:last-child')
                next_link.get_attribute("href")
                next_link.click()
                self.parse_content_url(self.driver.page_source)
                time.sleep(3)
                js = 'window.scrollTo(0,document.body.scrollHeight);'

                # 切换到主文档
                # 参考资料：selenium之 定位以及切换frame（iframe）
                # http://blog.csdn.net/huilan_same/article/details/52200586
                self.driver.switch_to.default_content()
                self.driver.execute_script(js)
                self.driver.switch_to.frame('iframeResult')
                self.crawl_next_page(self.driver.page_source)
            else:
                print('--- 爬虫停止 ---')
        else:
            print('------ 走到这里很可能是遇到验证码了 ------')
            try:
                check_code_input = self.driver.find_element_by_id("CheckCode")
                if check_code_input:
                    check_code = input('请输入您看到的验证码：')
                    check_code_input.send_keys(check_code)
                    submit_button = self.driver.find_element_by_xpath("//input[@type='button']")
                    submit_button.click()
                    self.crawl_next_page(self.driver.page_source)
            except Exception as e:
                print(e)
                self.crawl_next_page(self.driver.page_source)




    def crawl(self, target_url):
        self.driver.get(url=target_url)
        self.driver.maximize_window()
        self.select_fill_condition(self.driver)
        # 强制等待 5 秒，使得搜索结果出现（考虑是否可以写成显式的等待）

        time.sleep(10)
        js = 'window.scrollTo(0,document.body.scrollHeight);'
        self.driver.execute_script(js)

        self.driver.switch_to.frame('iframeResult')
        self.parse_content_url(self.driver.page_source)

        self.crawl_next_page(self.driver.page_source)

        # self.driver.close()


if __name__ == '__main__':
    cnkiSpider = CnkiSpider()
    # 起始的 url
    target_url = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CCND'
    cnkiSpider.crawl(target_url)
