import os
import platform

str = os.getcwd()
print(str)

# 当前文件的路径
pwd = os.getcwd()
print(pwd)
# 当前文件的父路径
father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")

print(father_path)
# 当前文件的前两级目录
grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
print(grader_father)

platform_system = platform.system()
print(platform_system)



