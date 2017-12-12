# 中国知网论文列表抓取

适合学习 Python 入门的教程：
1. 廖雪峰的 Python 教程
2. 菜鸟教程

本爬虫练习使用到的技术
1. 正则表达式
正则表达式是 Python 以及各种编程语言中非常重要的知识，正则表达式的语言是通用的，功能强大，可以用于字符串的查找、替换等，在学习中应该引起重视。
2. phantomjs、Selenium 浏览器模拟技术在爬虫中的应用
3. 使用 BeautifulSoup 解释 HTML 网页结构
4. os 和 path 也是很常用的库
5. 异常处理
6. 文件处理
7. csv 文件的保存与读取
8. pandas 处理 excel 如何追加数据


CSS 选择器官方文档：
http://www.w3school.com.cn/cssref/css_selectors.asp


如何运行代码：
1. 安装相关的软件
+ Python3
+ Anaconda 软件包集合（基于 Python3）
+ Selenium （安装了 Python3 以后使用 `pip install selenium`）
+ Selenium 的驱动：Chrome 或者 Firefox 的（非必需，因为 Selenium 自带了一个 Firefox 的驱动）
+ BeautifulSoup：用于解析 html 文档
+ 
2. 

**标题中有换行的一定要去掉。**

```python
# 网页正文全文高： document.body.scrollHeight
js = 'window.scrollTo(0,document.body.scrollHeight);'
driver.execute_script(js)
```

```python
with open('test.html', 'w', encoding='utf-8') as fw:
    fw.write(page_source)
```

@staticmethod 方法的含义：


参考资料：selenium之 定位以及切换frame（iframe）
http://blog.csdn.net/huilan_same/article/details/52200586


存在的问题：
1. 日志文件应该专门放在一个文件夹里；
2. 文件名修改

