# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 13:38
# @Author  : Mrli
# @File    : exceptions.py


class NetworkException(Exception):
    pass


class FeedInfoException(Exception):
    pass


class FileError(FileNotFoundError):
    pass
