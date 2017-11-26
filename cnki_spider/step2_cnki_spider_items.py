import datetime
from selenium import webdriver

from bs4 import BeautifulSoup
import csv
import re
from cnki_spider.spiderLog import SpiderLog


class CnkiSpiderItems:
    def __init__(self, file_name, start_num, end_num):
        self.log = SpiderLog()
        # 无界面浏览器
        self.driver = webdriver.PhantomJS(executable_path='/Users/liwei/phantomjs-2.1.1-macosx/bin/phantomjs')
        # 有界面浏览器
        # self.driver = webdriver.Firefox()
        self.start_num = start_num
        self.end_num = end_num
        self.file_name = file_name
        self.container = []

        self.subtitle_pattern = r'id="catalog_TI_SUB">副标题：</label>(.*?)</p>'
        self.publish_date_pattern = r'id="catalog_DATE">报纸日期：</label>(.*?)</p>'
        self.layer_name_pattern = r'id="catalog_LM">版名：</label>(.*?)</p>'
        self.layer_num_pattern = r'<label id="catalog_BH">版号：</label>(.*?)</p>'
        self.category_num_pattern = r'<label id="catalog_ZTCLS">分类号：</label>(.*?)</p>'

    def crawl_items(self):
        paper_links = self.read_paper_links()
        for paper in paper_links:
            items = paper.split(',')
            # count = items[0]
            # url = items[1]
            # title = items[2]
            self.driver.get(items[1])
            self.parse(items[0], self.driver.page_source)

    def read_paper_links(self):
        with open(self.file_name, 'r', encoding='utf-8') as fr:
            paper_links = fr.readlines()
            paper_links = paper_links[self.start_num: self.end_num]
        return paper_links

    # 使用正则表达式解析文本
    @staticmethod
    def parse_info(body, pattern):
        model = re.search(pattern, body)
        if model is None:
            return ''
        else:
            return model.group(1)

    def parse(self, index, page_source):
        line = []
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            # 1 正文标题
            title = soup.select('#mainArea h2.title')[0].text
        except Exception:
            title = ''
        try:
            # 2 副标题
            subtitle = self.parse_info(page_source, self.subtitle_pattern)
        except Exception:
            subtitle = ''
        try:
            # 3 正文快照，后面要加 [0]
            content_snapshot = soup.select('#ChDivSummary')[0].text
        except Exception:
            content_snapshot = ''
        try:
            # 4 报纸日期
            publish_date = self.parse_info(page_source, self.publish_date_pattern)
        except Exception:
            publish_date = ''
        try:
            # 5 版名
            layer_name = self.parse_info(page_source, self.layer_name_pattern)
        except Exception:
            layer_name = ''
        try:
            # 6 版号
            layer_num = self.parse_info(page_source, self.layer_num_pattern)
        except Exception:
            layer_num = ''
        try:
            # 7 分类号
            category_num = self.parse_info(page_source, self.category_num_pattern)
        except Exception:
            category_num = ''
        try:
            # 8 报纸名
            newspaper_name = soup.select('.sourinfo a[target="kcmstarget"]')[0].text
        except Exception:
            newspaper_name = ''
        try:
            # 9 报纸所在地
            newspaper_site = soup.select('.sourinfo p')[1].text
        except Exception:
            newspaper_site = ''
        try:
            # 10 报纸所在地地址
            newspaper_location = soup.select('.sourinfo p')[2].text
        except Exception:
            newspaper_location = ''
        try:
            # 11 报纸级别
            newspaper_level = soup.select('.sourinfo p')[3].text
        except Exception:
            newspaper_level = ''
        try:
            # 12 报纸网址
            newspaper_url = soup.select('.sourinfo a[target="kcmstarget"]')[1].text
        except Exception:
            newspaper_url = ''
            # 13 作者（要考虑到有多个作者的情况）
        try:
            author1 = ''
            author2 = ''
            author3 = ''
            author = soup.select('.author span')
            if len(author) == 1:
                author1 = author[0].text
            if len(author) == 2:
                author1 = author[0].text
                author2 = author[1].text
            if len(author) == 3:
                author1 = author[0].text
                author2 = author[1].text
                author3 = author[2].text
        except Exception:
            pass

        line_tuple = list((index, '联想', '品牌', '危机', title, subtitle, content_snapshot, publish_date, layer_name,
                           layer_num, category_num, newspaper_name, newspaper_site, newspaper_location,
                           newspaper_level, newspaper_url, author1, author2, author3))
        line.extend(line_tuple)
        self.container.append(line)
        arrive_end = int(self.end_num) == int(index)
        if len(self.container) % 5 == 0 or arrive_end:
            with open('output.csv', 'a', encoding='utf-8') as fw:
                writer = csv.writer(fw)
                for item in self.container:
                    writer.writerow(item)
                self.log.info("爬取了 {} 条数据。".format(index))
            self.container.clear()
        if arrive_end:
            self.log.info('到文件末尾了。')
            self.driver.close()


if __name__ == '__main__':
    # 可以换成无界面的浏览器，可能更快一些
    today = datetime.date.today().strftime('%Y-%m-%d')
    cnkiSpiderItems = CnkiSpiderItems(file_name='cnki_urls_{}.csv'.format(today), start_num=300, end_num=500)
    cnkiSpiderItems.crawl_items()
