from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Firefox(executable_path='/Users/liwei/geckodriver')
root_url = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CCND'
driver.get(root_url)

# 新建一个 Select 对象，通过这个对象帮助我们操作网页中的下拉列表
select1 = Select(driver.find_element_by_id('txt_1_sel'))
# 选择下拉列表中显示"主题"的那一项
select1.select_by_visible_text("主题")

# 找到特定的文本框，填写搜索条件
elem1 = driver.find_element_by_id('txt_1_value1')
elem1.send_keys('阿里巴巴')

# 找到特定的文本框，填写搜索条件
elem2 = driver.find_element_by_id('txt_1_value2')
elem2.send_keys('阿里')

# 新建一个 Select 对象，通过这个对象帮助我们操作网页中的下拉列表
select2 = Select(driver.find_element_by_id('txt_2_sel'))
# 选择下拉列表中显示"全文"的那一项
select2.select_by_visible_text("全文")

# 找到特定的文本框，填写搜索条件
elem3 = driver.find_element_by_id('txt_2_value1')
elem3.send_keys('品牌')

# 找到新增搜索条件的按钮，并点击
add_condition_link = driver.find_element_by_css_selector("#txt_1 .aomBtn a")
add_condition_link.click()

# 新建一个 Select 对象，通过这个对象帮助我们操作网页中的下拉列表
select3 = Select(driver.find_element_by_id('txt_3_sel'))
select3.select_by_visible_text("全文")

# 找到特定的文本框，填写搜索条件
elem4 = driver.find_element_by_id('txt_3_value1')
elem4.send_keys('危机')

# 将搜索按钮设置为焦点，并点击
search_button = driver.find_element_by_id('btnSearch')
search_button.click()
# 此时可以观察浏览器，如果结果没有出现，可以手点搜索按钮
# 强制等待 10 秒，使得搜索结果出现（考虑是否可以写成显式的等待）
time.sleep(10)
# 因为每页显示 50 条的链接在 iframe 里面，所以要将焦点切换
driver.switch_to.frame('iframeResult')
# 点击每页显示 50 条那个链接
driver.find_element_by_xpath("//div[@id='id_grid_display_num']/a[last()]").click()



