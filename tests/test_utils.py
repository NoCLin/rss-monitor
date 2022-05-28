# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 12:43
# @Author  : Mrli
# @File    : test_utils.py
from simplediff import html_diff

from monitor.utils import html_diff2, html_diff_to_markdown

old = "【全部公告本科生院 研究生院关于2020-2021学年秋冬学期课程调整安排的通知】 各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："
new = "【全部公告研究生院、本科生院 关于2020-2021学年秋冬学期课程调整安排的通知】 各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："


def test_html_diff2():
    r2 = html_diff2(old, new)
    assert r2 == "【全部公告<ins>研究生院、</ins>本科生院 <del>研究生院</del>关于2020-2021学年秋冬学期课程调整安排的通知】 各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："


def test_html_diff_to_markdown():
    r1 = html_diff(old, new)
    r3 = html_diff_to_markdown(r1)
    assert r3 == " **[-【全部公告本科生院 研究生院关于2020-2021学年秋冬学期课程调整安排的通知】-]**   **[+【全部公告研究生院、本科生院 关于2020-2021学年秋冬学期课程调整安排的通知】+]**  各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："
    r2 = html_diff2(old, new)
    r4 = html_diff_to_markdown(r2)
    assert r4 == "【全部公告 **[+研究生院、+]** 本科生院  **[-研究生院-]** 关于2020-2021学年秋冬学期课程调整安排的通知】 各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："
