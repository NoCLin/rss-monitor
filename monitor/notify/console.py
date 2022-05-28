from monitor.models import FeedItem
from monitor.notify.base import BaseNotify


class ConsoleNotify(BaseNotify):
    def __init__(self, config):
        super().__init__(config)

    def notify(self, item: FeedItem):
        title = ("New" if item.is_new else "Changed") + " " + item.title
        content = item.content[:200]
        link = item.link
        print(f"【{title}】{content}.... {link}")
