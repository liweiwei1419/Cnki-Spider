from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

# driver = webdriver.PhantomJS(executable_path='/Users/liwei/phantomjs-2.1.1-macosx/bin/phantomjs')
driver = webdriver.Chrome(executable_path='/Users/liwei/chromedriver')
driver.get("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CCND")

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

# 这一行代码很重要，将驱动的焦点转向子 iframe
# 这一行代码很重要，将驱动的焦点转向子 iframe
# 这一行代码很重要，将驱动的焦点转向子 iframe
driver.switch_to_frame('iframeResult')

# 等待网页加载
time.sleep(5)

print(driver.page_source)

with open('test.html','w',encoding='utf-8') as fw:
    fw.write(driver.page_source)

driver.quit()
