# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 12:29
# @File    : base.py
from typing import List

import feedparser
import requests
from retry import retry

from monitor.exceptions import FeedInfoException
from monitor.ext import LOG
from monitor.handler.configHandler import ConfigHandler
from monitor.handler.loggerHandler import LoggerHandler
from monitor.models import FeedItem
from monitor.notify.base import BaseNotify
from monitor.notify.console import ConsoleNotify
from monitor.notify.dingtalk import DingTalkNotify
from monitor.storage.base import BaseStorage
from monitor.storage.factory import StorageFactory
from monitor.utils.stru import format_file_path


class MonitorTask:
    """针对某个feed的任务详情"""

    def __init__(self, name, feed_url, interval, storage: BaseStorage, notifiers: List[BaseNotify], logger=None):
        self.name = name
        self.feed_url = feed_url
        self.interval = interval
        self.storage = storage
        self.notifies = notifiers
        self.logger = logger if logger else LOG
        self.logger.info(f"新建任务 {locals()}")

    @property
    def hash(self):
        return format_file_path(self.name + self.feed_url[-5:])[1]

    def check(self):
        self.logger.debug(f"{self.name} 正在检查更新")
        self.storage.read(task_hash=self.hash)

        @retry(tries=3)
        def fetch():
            self.logger.debug(f"{self.name} 正在抓取 {self.feed_url}")
            feed_text = requests.get(self.feed_url).text
            self.logger.debug(f"{self.name} 抓取成功")

            # 解析feed信息
            f = feedparser.parse(feed_text)
            assert not f.get("bozo_exception")
            feed_entries = f['entries']
            self.logger.debug(f"{self.name} 获取到{len(feed_entries)}条")

            if len(feed_entries) == 0:
                self.logger.error(f"{self.name} 获取到的feed为空")
                raise FeedInfoException(f"{self.name} 获取到的feed为空")

            return feed_entries

        feed_entries = fetch()

        # 检验是否有修改item
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
                self.logger.info(f"{self.name} {'新增' if item.is_new else '修改'}内容 {item.title} - {item.uuid}")
                changed_items.append(item)
        self.logger.info(f"{self.name} 检测到变化条目%d" % len(changed_items))

        # 第一次运行
        if self.storage.is_empty():
            self.logger.info(f"{self.name} 第一次运行, 加载已有数据。 本次不通知~")
        else:
            # 一次周期中允许最大的更新条目数量
            MAX_CHANGE_ITEMS = 10
            if len(changed_items) > MAX_CHANGE_ITEMS:
                self.logger.warning(f"{self.name} 周期内更新的条目太多, 大于{MAX_CHANGE_ITEMS}")
            else:
                # 将信息进行推送
                for item in changed_items:
                    for n in self.notifies:
                        @retry(tries=3)
                        def do_notify():
                            self.logger.info(f"{self.name} 正在通过{n}发送通知")
                            n.notify(item)

                        do_notify()
        self.storage.save(task_hash=self.hash)


class Runner:
    def __init__(self, config_filename, *args, **kwargs):
        self.logger = LoggerHandler(self.__get_logger_name())
        self.config = ConfigHandler(config_filename)
        self.storage = self._init_storage(self.config.storage["type"])

    def _init_storage(self, typ):
        return StorageFactory.create_storage(typ)

    def _get_notifiers(self, feed: dict):
        notifiers = []
        for n in feed["notifiers"]:
            # 全局的notifier配置
            notifier_config = self.config.notify.get(n["type"], {})
            self.logger.debug(f"global base_notifier: {notifier_config}")
            # 设置推送者
            notify_class = {
                "console": ConsoleNotify,
                "dingtalk": DingTalkNotify,
            }.get(n["type"])
            # 替换全局配置
            self.logger.debug(f"Feed {feed['name']} overwritten_notifier {notifier_config} as {n['type']}")
            # 实例化推送者
            notifier_ins = notify_class(notifier_config)
            notifiers.append(notifier_ins)
        return notifiers

    def _generate_tasks(self):
        # 根据feeds链接获得信息
        return [MonitorTask(name=feed["name"],
                            feed_url=feed["url"],
                            interval=feed.setdefault("interval", 0),
                            storage=self.storage,
                            notifiers=self._get_notifiers(feed),
                            logger=self.logger) for feed in self.config.feeds]

    def run(self):
        raise NotImplementedError

    def __get_logger_name(self) -> str:
        return self.__class__.__name__
