# 菜鸟教程 http://www.runoob.com/python/att-string-format.html

# 不设置指定位置，按默认顺序
str1 = "{} {}".format("hello", "world")
print(str1)

# 设置指定位置
str2 = "{0} {1}".format("hello", "world")
print(str2)

# 设置指定位置
str3 = "{1} {0} {1}".format("hello", "world")
print(str3)
