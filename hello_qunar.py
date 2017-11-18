from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


to_city ='上海'
fromdate = '2017-11-20'
todate = '2017-11-28'
# 驱动程序位置的配置 chromedriver
chromedriver = "/Users/liwei/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
# 让驱动程序帮助我们打开 去哪儿网
driver.get('http://hotel.qunar.com/')


try:
    WebDriverWait(driver,10).until(EC.title_contains(to_city))
except Exception as e:
    print(e)

time.sleep(5)
js = 'window.scrollTo(0,document.body.scrollHeight);'
driver.execute_script(js)
driver.close()




