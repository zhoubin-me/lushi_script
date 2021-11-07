# -*- coding: utf-8 -*-

import logging
import os
import sys
from datetime import datetime


class LoggingUtil:
    def __init__(self):
        # python官方文档中提供的一段示例，使用logging模块产生logger对象
        LOG_FORMAT = "%(asctime)s [%(levelname)7s] %(thread)d --- %(filename)s:%(lineno)d  : %(message)s"
        logging.basicConfig(format=LOG_FORMAT)
        # 创建一个日志对象，这个参数可以随便填，这个参数唯一标识了这个日志对象
        self.logger = logging.getLogger()
        # 设置级别
        self.logger.setLevel(logging.INFO)

        current_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # print(current_path)
        # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把log变成文件名的一部分了
        log_path = os.path.join(current_path, 'logs')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # 指定输出的日志文件名
        dt = datetime.strftime(datetime.now(), "%Y-%m-%d_%H")
        # 日志的文件名
        log_name = log_path + '/' + str(dt) + '.log'
        # 创建一个handler，用于写入日志文件, 'a'表示追加
        file_handler = logging.FileHandler(log_name, 'a', encoding='utf-8')
        # 为logger添加的日志处理器
        self.logger.addHandler(file_handler)
        log_format = logging.Formatter(LOG_FORMAT)
        # 设置日志内容的格式
        file_handler.setFormatter(log_format)
        console_handler = logging.StreamHandler(stream=sys.stdout)
        self.logger.addHandler(console_handler)

    def test(self):
        self.logger.error("这个一条错误日志")
        self.logger.info("这是一条info日志")
        self.logger.debug("这是一条debug日志")
        self.logger.warning("这是一条warning日志")


LoggingUtil()
logger = logging.getLogger()


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))  # 重点


sys.excepthook = handle_exception  # 重点

if __name__ == '__main__':
    log = LoggingUtil()
