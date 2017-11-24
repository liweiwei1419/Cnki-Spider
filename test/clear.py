import os

file_name = 'hello.xls'

if os.path.exists(file_name):
    os.remove(file_name)
else:
    print('文件不存在，什么也不做')

# 删除文件
# os.remove("aaaa")

# 判断否则文件是否存在
# exists1 = os.path.exists("pager1.html")
# print(exists1)


for i in range(1,21):
    file_name = "pager{}.html".format(i)
    if os.path.exists(file_name):
        os.remove(file_name)
