import logging
import getpass

import sys


class SpiderLog:
    def _get_log_path(self):
        file_path = sys.argv[0]
        divide_index = file_path.rindex('/')
        log_path = file_path[:divide_index] + '/logs/' + file_path[file_path.rindex('/') + 1:-3] + '.log'
        return log_path

    def __init__(self):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)

        logFile = self._get_log_path()
        formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')

        logHand = logging.FileHandler(logFile, encoding='utf8')
        logHand.setFormatter(formatter)
        logHand.setLevel(logging.ERROR)

        logHandst = logging.StreamHandler()
        logHandst.setFormatter(formatter)
        logHandst.setLevel(logging.DEBUG)

        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandst)

    # 日志的 5 个级别对应一下的 5 个函数
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    mylog = SpiderLog()
    mylog.debug("I'm debug 测试中文")
    mylog.info("I'm info")
    mylog.warn("I'm warm")
    mylog.error("I'm error 测试中文")
    mylog.critical("I'm critical")
