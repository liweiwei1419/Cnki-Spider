import datetime
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from test.bs4_test import BeautifulSoup


class QunaSpider:
    def get_hotel(self, driver, to_city, fromdate, todate):
        ele_toCity = driver.find_element_by_name('toCity')
        ele_fromDate = driver.find_element_by_id('fromDate')
        ele_toDate = driver.find_element_by_id('toDate')

        # class="search-button js_btnsearch" 定位的时候只须要写其中一个 class 的名字就可以了
        ele_search = driver.find_element_by_class_name('search-button')

        ele_toCity.clear()
        ele_toCity.send_keys(to_city)
        # 这句话的作用是什么？
        ele_toCity.click()

        ele_fromDate.clear()
        ele_fromDate.send_keys(fromdate)

        ele_toDate.clear()
        ele_toDate.send_keys(todate)

        ele_search.click()

        page_num = 0

        while True:
            try:
                WebDriverWait(driver, 10).until(EC.title_contains(to_city))
            except Exception as e:
                print(e)
            time.sleep(5)
            js = 'window.scrollTo(0,document.body.scrollHeight);'
            driver.execute_script(js)
            html_const = driver.page_source
            soup = BeautifulSoup(html_const, 'html.parser', from_encoding='utf-8')
            infos = soup.find_all(class_='item_hotel_info')

            # f = codecs.open(to_city + fromdate + '.html', 'a', 'utf-8')

            try:
                next_page = WebDriverWait(driver,10).until(EC.visibility_of(driver.find_element_by_css_selector('.item.next')))
                time.sleep(5)
                next_page.click()
                page_num +=1

            except Exception as e:
                print(e)

    def crawl(self, root_url, to_city):
        today = datetime.date.today().strftime('%Y-%m-%d')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        # 设置 chrome 补丁文件的路径
        driver = webdriver.Chrome(executable_path='/Users/liwei/chromedriver')
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        # 将浏览器最大化显示
        # driver.maximize_window()
        # 控制时间间隔，等待浏览器反映（这是什么意思呢）
        driver.implicitly_wait(10)
        self.get_hotel(driver, to_city, today, tomorrow)


if __name__ == '__main__':
    spider = QunaSpider()
    spider.crawl('http://hotel.qunar.com/', u'上海')
