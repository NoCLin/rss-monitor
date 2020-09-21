# encoding: utf-8
import json
import sys

import feedparser
import fire
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
from retrying import retry

from models import FeedItem
from notify.console import ConsoleNotify
from notify.dingtalk import DingTalkNotify
from storage.memory import MemoryStorage


class MonitorTask():
    def __init__(self, name, feed_url, interval, storage, notifiers):
        self.name = name
        self.feed_url = feed_url
        self.interval = interval
        self.storage = storage
        self.notifies = notifiers

        self.first_run = True
        logger.info(f"新建任务 {locals()}")

    def check(self):

        logger.debug("{name} 正在检查更新", name=self.name)

        @retry(stop_max_attempt_number=3)
        def fetch():
            logger.debug(f"{self.name} 正在抓取" + self.feed_url)
            feed_text = requests.get(self.feed_url).text
            logger.debug(f"{self.name} 抓取成功")
            f = feedparser.parse(feed_text)
            assert not f.get("bozo_exception")
            feed_entries = f['entries']
            logger.debug(f"{self.name} 获取到{len(feed_entries)}条")

            if len(feed_entries) == 0:
                logger.error(f"{self.name} 获取到的feed为空")
                raise Exception()

            return feed_entries

        feed_entries = fetch()

        changed_items = []
        for e in feed_entries:

            item = FeedItem()
            item.title = e["title"]
            item.uuid = e['id']
            item.link = e['link']
            item.content = e['summary']
            item.full_content = f"【{item.title}】 {item.content}"
            last = self.storage.get(item.uuid)

            if last != item.full_content:
                self.storage.set(item.uuid, item.full_content)
                item.is_new = (last is None)
                item.old_full_content = last

                logger.info(f"{self.name} {'新增' if item.is_new else '修改'}内容 {item.title} - {item.uuid}")

                changed_items.append(item)

        logger.info(f"{self.name} 检测到变化条目%d" % len(changed_items))

        if self.first_run:
            logger.info(f"{self.name} 第一次运行，不通知")
            self.first_run = False
            return

        if len(changed_items) > 5:
            logger.warning(f"{self.name} 周期内更新的条目太多")
        else:
            for item in changed_items:
                for n in self.notifies:
                    @retry(stop_max_attempt_number=3)
                    def do_notify():
                        logger.info(f"{self.name} 正在通过{n}发送通知")
                        n.notify(item)

                    do_notify()


def init_storage(storage_config):
    t = storage_config["type"]
    s = {
        "memory": MemoryStorage
    }.get(t)(storage_config)
    return s


def main(config_file="config.json"):
    logger.remove()
    logger.add(sink='logs/debug.log', format="{time} - {level} - {message}", level="DEBUG",
               backtrace=True, diagnose=True,
               encoding="utf-8",
               rotation="50 MB"
               )
    logger.add(sink=sys.stderr, level="INFO")

    logger.info(f"using config file {config_file}")
    with open(config_file, "rt") as f:
        config = json.load(f)

    tasks = []
    storage = init_storage(config["storage"])
    global_notifiers = config["notify"]

    for feed in config["feeds"]:

        notifiers = []

        for n in feed["notifiers"]:
            notifier_config = global_notifiers.get(n["type"], {})
            logger.debug(f"base_notifier{notifier_config}")
            notify_class = {
                "console": ConsoleNotify,
                "dingtalk": DingTalkNotify,

            }.get(n["type"])

            notifier_config.update(n)  # 更新任务中对全局进行覆盖的配置
            logger.debug(f"overwritten_notifier{notifier_config}")

            notifier_ins = notify_class(notifier_config)
            notifiers.append(notifier_ins)

        task = MonitorTask(name=feed["name"],
                           feed_url=feed["url"],
                           interval=feed["interval"],
                           storage=storage,
                           notifiers=notifiers)
        tasks.append(task)

    # Schedule task
    scheduler = BlockingScheduler()

    for task in tasks:
        task.check()  # 立即执行一次
        scheduler.add_job(task.check, 'interval', name=task.name, seconds=task.interval, max_instances=1)
        logger.info(f"添加任务 {task.name}(检测间隔{task.interval}s) {task.feed_url}")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    fire.Fire(main)
