# 中国知网论文列表抓取

存在的问题：
1. 日志文件应该专门放在一个文件夹里；
2. 文件名修改

1. Python 对字符串的处理
2. 正则表达式
3. 使用 Scrapy 的 Selector 和 BeautifulSoup 的选择器的不同
4. 迭代器
5. yield 关键字的使用
6. 通过查看源代码来查看可以使用的 API
7. 先把功能实现，再优化，很多细节问题会在优化的时候解决
8. os 和 path 也是很常用的库
9. PyCharm 增加注释与取消注释
10. 批量删除文件
11. os 拼凑成绝对路径
12. 异常处理
13. pandas 处理 excel 如何追加数据


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

