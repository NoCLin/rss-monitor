# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 12:30
# @Author  : Mrli
# @File    : runner.py

from monitor.runner.base import Runner
from monitor.storage.factory import FactoryEnum, StorageFactory
from settings import PROJECT_DIR


class DirectRunner(Runner):

    def _init_storage(self, typ):
        return StorageFactory.create_storage(FactoryEnum.JsonFile)

    def run(self):
        """开启定时任务"""
        tasks = self._generate_tasks()
        for task in tasks:
            # 立即执行一次, 将数据全部加入Storage, 之后再次运行时就是新的增量数据
            task.check()


if __name__ == '__main__':
    runner = DirectRunner(PROJECT_DIR.joinpath("config.demo.json"))
    runner.run()
