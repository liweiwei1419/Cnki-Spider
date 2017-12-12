import platform
import os


class Utils():
    @staticmethod
    def get_selenium_file_path():
        if 'Windows' in platform.system():
            pwd = os.getcwd()
            father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
            selenium_file_path = father_path + os.path.sep + "geckodriver-v0.19.1-win64" + os.path.sep + 'geckodriver.exe'
            print(selenium_file_path)
            return selenium_file_path
        else:
            return '/Users/liwei/geckodriver'
