import requests
from bs4 import BeautifulSoup
from loguru import logger

from models import FeedItem
from .base import BaseNotify


def send_text_msg(url, text):
    r = requests.post(url, json={"msgtype": "text", "text": {"content": "%s" % text}})
    assert r.json()


def send_action_card(ding_url, title, text, btnOrientation, btns=None):
    """

    :param ding_url:
    :param title:
    :param text:
    :param btnOrientation: "0"
    :param btns: [
                {"title": "", "actionURL": ""}
            ]
    :return:
    """
    if btns is None:
        btns = []
    data = {
        "actionCard": {
            "title": title,
            "text": text,
            "btnOrientation": btnOrientation,
            "btns": btns
        },
        "msgtype": "actionCard"
    }

    r = requests.post(ding_url, json=data)
    if r.json().get("errcode"):
        raise Exception("请求出错" + r.text)


class DingTalkNotify(BaseNotify):
    def __init__(self, config):
        super().__init__(config)

        self.url = config["send_url"]
        self.message_type = config["message_type"]
        assert self.url
        assert self.message_type

    # 网络错误 retry
    # @retrying.retry()
    def notify(self, item: FeedItem):

        title = ("New" if item.is_new else "Changed") + " " + item.title
        content = item.content
        content = BeautifulSoup(content, 'html.parser').get_text()[:200]
        link = item.link


        if self.message_type == "text":
            send_text_msg(self.url, f"【{title}】{content}.... {link}")
            return
        if self.message_type == "actionCard":
            logger.info(f"正在发送 【{title}】{content}.... {link}")

            # 网络错误 retry
            send_action_card(self.url, title=title, text=f"【{title}】{content}.... {link}",
                             btnOrientation=0,
                             btns=[
                                 {"title": "查看原文", "actionURL": link}
                             ])
            return

        raise Exception("Unknown Message Type " + self.message_type)

