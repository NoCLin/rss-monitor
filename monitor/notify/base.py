from monitor.models import FeedItem


class BaseNotify:

    def __init__(self, config):
        self.config = config
        pass

    def notify(self, item: FeedItem):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self.config})"

    def __repr__(self):
        return self.__str__()
