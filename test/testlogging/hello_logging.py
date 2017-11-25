import logging
import getpass
import sys


class MyLog:
    def __init__(self):
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        # 这里设置日志的级别
        self.logger.setLevel(logging.DEBUG)
        logFile = './' + sys.argv[0][0:-3] + '.log'  # 日志文件名
        formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')

        # FileHandler
        logHand = logging.FileHandler(logFile)  # 指定文件名
        logHand.setFormatter(formatter)  # 指定格式
        logHand.setLevel(logging.ERROR)  # 指定级别，只有 error 以及 error 以上的级别才会被记录到日志中

        logHandSt = logging.StreamHandler()
        logHandSt.setFormatter(formatter)  # 指定格式

        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandSt)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    myLog = MyLog()
    myLog.debug("debug message")
    myLog.info("info message")
    myLog.warn("warn message")
    myLog.error("error message")
    myLog.critical("critical message")
