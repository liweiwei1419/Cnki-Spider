from selenium import webdriver
import os

# chromedriver = "/Users/liwei/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver

# phantomjs 是一款无界面的浏览器
driver = webdriver.PhantomJS(executable_path='/Users/liwei/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.get("http://hotel.qunar.com/")

data = driver.title
print(data)
