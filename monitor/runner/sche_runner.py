# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 12:30
# @File    : sche_runner.py


from monitor.runner.base import Runner


class ScheRunner(Runner):
    def run(self):
        from apscheduler.schedulers.blocking import BlockingScheduler

        """开启定时任务"""
        scheduler = BlockingScheduler()
        tasks = self._generate_tasks()
        for task in tasks:
            # 立即执行一次, 将数据全部加入Storage, 之后再次运行时就是新的增量数据
            task.check()
            scheduler.add_job(task.check, 'interval', name=task.name, seconds=task.interval, max_instances=1)
            self.logger.info(f"添加任务 {task.name}(检测间隔{task.interval}s) {task.feed_url}")

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
