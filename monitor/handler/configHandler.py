# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 12:53
# @Author  : Mrli
# @File    : ConfigHandler.py
import json

from monitor.utils.singleton import Singleton


class ConfigHandler(metaclass=Singleton):

    def __init__(self, config_file):
        self.config = {}
        with open(config_file, "rt", encoding="utf8") as f:
            self.config = json.load(f)

    @property
    def storage(self):
        return self.config["storage"]

    @property
    def notify(self):
        return self.config["notify"]

    @property
    def feeds(self) -> dict:
        return self.config["feeds"]
