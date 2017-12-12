import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from cnki_spider.spiderLog import SpiderLog
import datetime


class CnkiSpider:
    def __init__(self, root_url, max_crawl_page, max_crawl_items):
        '''

        :param root_url: 爬虫入口的链接
        :param max_crawl_page: 最多爬取的页码数
        :param max_crawl_items: 最多爬取的数据条数
        '''
        # 设置日志，可以使用 print("") 语句代替
        self.log = SpiderLog()
        # 设置一些控制爬虫的参数
        self.current_page = 1
        self.current_last_item_num = 0
        self.max_crawl_page = max_crawl_page
        self.max_crawl_items = max_crawl_items

        self.file_name = "papers_urls_{}.csv".format(datetime.date.today().strftime('%Y-%m-%d'))
        self.log.info('--- 初始化：设置 Chrome 或者 Firefox 补丁文件的路径 ---')
        # Chrome 或者 Firefox 二者设置一个就可以了，
        # executable_path 要替换成自己本机上的驱动地址
        # 设置 Chrome 补丁文件的路径
        # self.driver = webdriver.Chrome(executable_path='/Users/liwei/chromedriver')
        # 设置 Firefox 补丁文件的路径
        # 本类中其它方法要使用 driver 的时候，可以通过 self.driver 进行调用
        # self.driver = webdriver.Firefox(executable_path="C:\\liwei\\geckodriver-v0.19.1-win64\\geckodriver.exe")
        self.driver = webdriver.Firefox(executable_path='/Users/liwei/geckodriver')
        # 让浏览器访问网页
        self.driver.get(url=root_url)
        # 让窗口最大化，使得驱动能够"看到"更多的内容
        self.driver.maximize_window()

    def select_fill_condition(self):
        '''
        让驱动帮我们：
        1、设置搜索条件
        2、点击提交按钮
        3、点击每页显示 50 条数据（这样每一页可以爬取更多的 url）
        :param driver:
        :return:
        '''
        # 新建一个 Select 对象，通过这个对象帮助我们操作网页中的下拉列表
        select1 = Select(self.driver.find_element_by_id('txt_1_sel'))
        # 选择下拉列表中显示"主题"的那一项
        select1.select_by_visible_text("主题")

        # 找到特定的文本框，填写搜索条件
        elem1 = self.driver.find_element_by_id('txt_1_value1')
        elem1.send_keys('阿里巴巴')

        # 找到特定的文本框，填写搜索条件
        elem2 = self.driver.find_element_by_id('txt_1_value2')
        elem2.send_keys('阿里')

        # 新建一个 Select 对象，通过这个对象帮助我们操作网页中的下拉列表
        select2 = Select(self.driver.find_element_by_id('txt_2_sel'))
        # 选择下拉列表中显示"全文"的那一项
        select2.select_by_visible_text("全文")

        # 找到特定的文本框，填写搜索条件
        elem3 = self.driver.find_element_by_id('txt_2_value1')
        elem3.send_keys('品牌')

        # 找到新增搜索条件的按钮，并点击
        add_condition_link = self.driver.find_element_by_css_selector("#txt_1 .aomBtn a")
        add_condition_link.click()

        # 新建一个 Select 对象，通过这个对象帮助我们操作网页中的下拉列表
        select3 = Select(self.driver.find_element_by_id('txt_3_sel'))
        select3.select_by_visible_text("全文")

        # 找到特定的文本框，填写搜索条件
        elem4 = self.driver.find_element_by_id('txt_3_value1')
        elem4.send_keys('危机')

        # 将搜索按钮设置为焦点，并点击
        search_button = self.driver.find_element_by_id('btnSearch')
        search_button.click()
        # 此时可以观察浏览器，如果结果没有出现，可以手点搜索按钮
        # 强制等待 10 秒，使得搜索结果出现（考虑是否可以写成显式的等待）
        self.log.info("等待 10 秒，等到搜索结果出现")
        time.sleep(10)
        # 因为每页显示 50 条的链接在 iframe 里面，所以要将焦点切换
        self.driver.switch_to.frame('iframeResult')
        # 点击每页显示 50 条那个链接
        try:
            self.driver.find_element_by_xpath("//div[@id='id_grid_display_num']/a[last()]").click()
        except Exception:
            self.log.warn("第 1 页上没有找到\"每页显示 50 条\"的链接。重新尝试。")

    def save_urls(self, table):
        rows = table[1:]
        # 'a' 表示追加，这里明显应该使用追加的方式保存数据
        with open(self.file_name, 'a', encoding='utf-8', newline='') as fw:
            writer = csv.writer(fw)
            for row in rows:
                order_number = row.select('td')[0].text
                href = row.select('a')[0].get('href')
                title = row.select('a')[0].text
                writer.writerow([order_number, self.handle_url(href), self.handle_title(title)])
                # writer.writerow(list((order_number, self.handle_url(href), self.handle_title(title))))
            self.current_last_item_num = order_number
        self.log.info("第 {} 页的文章链接爬取成功，最后一条记录的编号是：{}。".format(self.current_page, self.current_last_item_num))

    def judge_if_continue(self):
        '''
        写完文件以后作判断是否继续
        :return:
        '''
        if self.max_crawl_page is not None:
            if self.current_page == self.max_crawl_page + 1:  # +1 是因为保存了 urls 以后，current_page 马上就加 1 了
                self.log.info("已经爬取了 {} 页，爬虫因为设定了【最多爬取页数】停止。".format(self.max_crawl_page))
                return False
        if self.max_crawl_items is not None:
            if int(self.current_last_item_num) >= int(self.max_crawl_items):
                self.log.info("已经爬取了 {} 条记录，爬虫因为设置了【最多爬取条数】停止。".format(self.current_last_item_num))
                return False
        return True

    def parse(self):
        '''
        点击了搜索按钮以后的入口
        :return:
        '''
        # "lxml" 必须指定，这是官方推荐的解释器
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        table = soup.select('.GridTableContent tr')
        # 如果当前页面上有表格，就爬取表格中的序号、标题和链接到 csv 文件中
        if table:
            # 页面上显示的当前页的页面
            html_current_page = soup.select('table.pageBar_bottom font[class="Mark"]')[0].get_text()
            # 因为 Selenium 的点击链接事件有的时候会失效，
            # 所以需作判断，让页面显示的页数，也我们逻辑上应该显示的页数一致的时候，才保存页面的内容
            # 这样做是为了防止重复爬取
            if int(html_current_page) == int(self.current_page):
                self.save_urls(table)
                self.current_page += 1
            if not self.judge_if_continue():
                return

            # 写完文件以后，如果不满足爬取完成的条件，就判断是否有"下一页"按钮
            # 判断是否有下一页：
            # 所有 a 标签的集合
            a_list = soup.select('div.TitleLeftCell a')
            if a_list:
                next_link = a_list[-1]
                if next_link.get_text() == '下一页':
                    # 点击'下一页'按钮，并且继续爬取
                    self.click_next_and_parse()
                else:
                    self.log.error("第 {} 页上没有出现\"下一页\"按钮，爬虫结束。".format(self.current_page))
            else:
                # 如果第一页就显示出了所有的结果
                self.log.info("所有的查询结果在第一页就显示完毕，一共查询到数据 {} 条。".format(self.current_last_item_num))
                return
        else:
            # 有可能是要求输入验证码的页面
            self.log.warn('------ 走到这里很可能是遇到验证码了，请回到网页查看，并在控制台中输入验证码。 ------')
            # 用户手动输入验证码，实现翻页
            self.input_captcha_by_ourself()

    def click_next_and_parse(self):
        # 有下一页按钮
        self.log.info("当前第 {} 页，有下一页按钮。".format(self.current_page - 1))  # 这里 -1 也是因为有一个偏差
        # 注意：要将页面定位到页面底端，Selenium 才会帮我们点击按钮
        # 点击下一页按钮
        next_link = self.driver.find_element_by_css_selector('div.TitleLeftCell a:last-child')
        # next_link_str = next_link.get_attribute("href")
        next_link.click()  # 这个点击按钮有的时候可能没有生效，会重复爬取数据
        # 切换到主文档
        self.driver.switch_to.default_content()
        js = 'window.scrollTo(0,document.body.scrollHeight);'
        self.driver.execute_script(js)
        # 切换到子 iframe
        self.driver.switch_to.frame('iframeResult')
        # 递归调用（自己调用自己）
        self.parse()

    def input_captcha_by_ourself(self):
        '''
        用户手动输入验证码，实现翻页
        :return:
        '''

        # 1、回到主窗口
        self.driver.switch_to.default_content()
        # 回到页面顶端的位置，这样可以看到验证码
        js = 'window.scrollTo(0,0);'
        self.driver.execute_script(js)
        # 2、再回到子 iframe
        self.driver.switch_to.frame('iframeResult')
        # 检测是否有输入验证码的输入框
        check_code_input = self.driver.find_element_by_id("CheckCode")
        # 如果有输入框
        if check_code_input:
            check_code = input('请输入您在页面中看到的验证码：')
            check_code_input.send_keys(check_code)
            submit_button = self.driver.find_element_by_xpath("//input[@type='button']")
            submit_button.click()
            # 如果验证码出错，我们还会看到要求输入验证码的页面，逻辑包含在 parse 中了
            self.parse()
        else:
            # 如果出现下面这行日志，就表示代码写得有问题
            self.log.warn('------ 没有验证码输入框，也没有表格，程序错误，退出。 ------')
            return

    def crawl(self):
        # 第 1 步：首先执行的是构造方法 __init__(self)，其中含有一些初始化的逻辑
        # __init__(self) 是默认执行的，不需要显示调用，需要把实现的逻辑写在 __init__(self) 方法里
        # 第 2 步：填写网页上的搜索条件
        self.select_fill_condition()
        # 第 3 步：如果有下一页按钮，则点击下一页按钮，重复执行第 3 步和第 4 步
        # parse 方法是一个递归方法，即自己调用自己，递归结束的条件是页面上没有"下一页"按钮，或者满足爬取的最多页数和最多条数，爬虫停止
        self.parse()
        self.driver.close()

    @staticmethod
    def handle_title(title):
        '''
        去掉标题中的空行，这样能保证一条数据保存在 csv 文件中的一行内
        :param title:
        :return:
        '''
        return title.replace('\n', '').replace(' ', '')

    @staticmethod
    def handle_url(url):
        return "http://kns.cnki.net/KCMS" + url[4:]


if __name__ == '__main__':
    # root_url: 起始的 url
    # max_crawl_page: 最多爬取的页码数
    # max_crawl_items: 最多爬取的数据条数
    root_url = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CCND'
    cnkiSpider = CnkiSpider(root_url=root_url, max_crawl_page=None, max_crawl_items=None)
    cnkiSpider.crawl()
