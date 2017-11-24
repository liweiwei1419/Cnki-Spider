# 在 Python 中，glob 模块是用来查找匹配的文件的
import glob
result = glob.glob('./*.py')
for item in result:
    print(item)