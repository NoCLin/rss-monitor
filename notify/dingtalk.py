import requests
from loguru import logger

from models import FeedItem
from utils import html_diff_to_markdown, html_diff2, html_to_text, shorten
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

    def notify(self, item: FeedItem):

        if item.is_new:
            full_content = html_to_text(item.full_content)
        else:
            old = html_to_text(item.old_full_content)
            new = html_to_text(item.full_content)
            full_content = html_diff_to_markdown(html_diff2(old, new))

        link = item.link
        title = item.title
        is_new_text = ('New' if item.is_new else 'Changed')
        full_content = shorten(full_content, 8000)

        if self.message_type == "text":
            send_text_msg(self.url, f"【{is_new_text}】{full_content}.... {link}")
            return
        if self.message_type == "actionCard":
            logger.info(f"正在发送 {full_content}.... {link}")

            send_action_card(self.url,
                             title=f"【{is_new_text}】 {title}",
                             text=f"【{is_new_text}】 {full_content} {link}",
                             btnOrientation=0,
                             btns=[
                                 {"title": "查看原文", "actionURL": link}
                             ])
            return

        raise Exception("Unknown Message Type " + self.message_type)
