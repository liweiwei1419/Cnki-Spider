from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path='/Users/liwei/chromedriver')

driver.get("http://baidu.com/")

elem = driver.find_element_by_name('wd')
elem.clear()

elem.send_keys("网络爬虫")
elem.send_keys(Keys.RETURN)

# 显式等待：条件出发式的等待

page_num = 1
while (True):
    if page_num == 6:
        break
    try:
        # 设置超时的时间为 10 秒，WebDriverWait 会默认 500ms 检测一下元素是否存在
        # expected_conditions 表示等待条件
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'n')))
    except Exception:
        print('在第 {} 页中没有找到"下一页"按钮'.format(page_num))
        break

    js = 'window.scrollTo(0,document.body.scrollHeight);'
    driver.execute_script(js)
    print("页面第 {} 页滑动到底端".format(page_num))

    try:
        # CSS 选择器中，有 > 表示只选择一代，没有大于号，表示连孙子节点都会被选到
        next_page = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of(driver.find_element_by_css_selector('#page > a:nth-last-child(1)')))
        next_page.click()
        page_num += 1
        time.sleep(3)
    except Exception:
        print('在第 {} 页没有找到"下一页"按钮点击失败'.format(page_num))
        break

driver.close()
