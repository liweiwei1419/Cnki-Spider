from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os

# 设置 chrome 补丁文件的路径
chromedriver = "/Users/liwei/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
driver.get('http://baidu.com/')

elem = driver.find_element_by_name('wd')
elem.clear()

elem.send_keys('网络爬虫')
elem.send_keys(Keys.RETURN)


WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"n")))

js = 'window.scrollTo(0,document.body.scrollHeight);'
driver.execute_script(js)

next_page = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_css_selector('.n')))
next_page.click()

#time.sleep(3)
#driver.close()
