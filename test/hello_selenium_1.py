from selenium import webdriver

# browser = webdriver.Chrome() 就不行，因为没有指定驱动
# selenium 自带了一个火狐浏览器的驱动
browser = webdriver.Firefox()
browser.get('http://www.fairphone.com/we-are-fairphone')
# 最大化打开的浏览器，这会帮助 Selenium 看到更多的内容
browser.maximize_window()