# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 12:52
# @Author  : Mrli
# @File    : logger.py
import sys

from loguru import logger

from settings import PROJECT_DIR


class LoggerHandler:
    """
    将loguru中的单例固定下来
    """

    def __init__(self, logger_name="debug"):
        # 创建目录文件夹
        log_dir = PROJECT_DIR.joinpath("logs")
        if not log_dir.exists():
            log_dir.mkdir()

        logger.add(sink=log_dir.joinpath(f'{logger_name}.log'), format="{time} - {level} - {message}", level="DEBUG",
                   backtrace=True, diagnose=True,
                   encoding="utf-8",
                   rotation="20 MB",
                   filter=lambda x: logger_name in x
                   )
        logger.add(sink=sys.stderr, level="INFO")

    @property
    def LOG(self):
        return logger

# import logging
# import platform
# from logging.handlers import TimedRotatingFileHandler
#
# from settings import LOG_DIR
#
#
# class LoggerHandler(logging.Logger):
#     """
#     LogHandler
#     """
#
#     def __init__(self, name, level=logging.DEBUG, stream=True, file=True):
#         self.name = name
#         self.level = level
#         logging.Logger.__init__(self, self.name, level=level)
#         if stream:
#             self.__setStreamHandler__()
#         if file:
#             if platform.system() != "Windows":
#                 self.__setFileHandler__()
#
#     def __setFileHandler__(self, level=None):
#         """
#         set file handler
#         :param level:
#         :return:
#         """
#         file_name = LOG_DIR.joinpath(f'{self.name}.log')
#         # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
#         file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
#         file_handler.suffix = '%Y%m%d.log'
#         if not level:
#             file_handler.setLevel(self.level)
#         else:
#             file_handler.setLevel(level)
#         formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
#
#         file_handler.setFormatter(formatter)
#         self.file_handler = file_handler
#         self.addHandler(file_handler)
#
#     def __setStreamHandler__(self, level=None):
#         """
#         set stream handler
#         :param level:
#         :return:
#         """
#         stream_handler = logging.StreamHandler()
#         formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
#         stream_handler.setFormatter(formatter)
#         if not level:
#             stream_handler.setLevel(self.level)
#         else:
#             stream_handler.setLevel(level)
#         self.addHandler(stream_handler)
