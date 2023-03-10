# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 14:01
# @Author  : Mrli
# @File    : settings.py
from pathlib import Path
# 项目目录
PROJECT_DIR = Path(__file__).resolve().parent
# 默认
AVAILABLE_RUNNER_CHOICE = ["direct", "sche"]
# 默认配置
DEFAULT_CONFIG_FILE = "config.demo.json"
# 缓存文件
CACHE_FILE_DIR = PROJECT_DIR.joinpath("caches")
CACHE_FILE_DIR.mkdir(exist_ok=True)
# 日志文件
LOG_DIR = PROJECT_DIR.joinpath("logs")
LOG_DIR.mkdir(exist_ok=True)
