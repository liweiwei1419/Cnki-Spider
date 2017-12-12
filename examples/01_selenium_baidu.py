from selenium import webdriver
import time
import platform
import os


def get_selenium_file_path():
    if 'Windows' in platform.system():
        pwd = os.getcwd()
        father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
        selenium_file_path = father_path + os.path.sep + "geckodriver-v0.19.1-win64" + os.path.sep + 'geckodriver.exe'
        print(selenium_file_path)
        return selenium_file_path
    else:
        return '/Users/liwei/geckodriver'


# 使用 Selenium 以及相应的浏览器驱动程序帮助我们打开网页，并且获取源代码
# 不同的浏览器须使用不同的驱动程序，常用的有谷歌浏览器和火狐浏览器
# 驱动下载地址：

# 1、启动浏览器驱动程序
# 驱动下载以后，须要将驱动的地址配置到下一行代码中的 executable_path 变量中
driver = webdriver.Firefox(executable_path=get_selenium_file_path())

# 2、让浏览器打开网页
driver.get('https://www.baidu.com/')
# 3、将下载的网页的源代码保存到变量 content 中
content = driver.page_source
# 4、打印 content，可以看到，得到的 content 与在网页上右键"查看源代码"的内容是一致的
print('网页的内容是', content)
# 5、time.sleep(3) 代码的作用是让程序暂停在这一行，暂停的时间是 3 秒
# 如果须要暂停 5 秒，就写成 time.sleep(5)
time.sleep(3)
# 6、关闭浏览器
driver.close()
