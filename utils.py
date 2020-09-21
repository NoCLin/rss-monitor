from bs4 import BeautifulSoup
from simplediff import html_diff


def html_diff2(original, edited):
    import difflib
    d = difflib.Differ()
    # 直接按字切割，不做分词，分段
    diff = d.compare(original, edited)

    diff = list(diff)

    last_flag = diff[0][0]
    last_store = ""
    result = []
    for i in diff:
        flag, _, char = i
        if flag != last_flag:
            result.append((last_flag, last_store))
            last_store = ""

        last_store += char
        last_flag = flag
    result.append((last_flag, last_store))

    # print(result)

    result_html = ""

    for flag, text in result:
        if flag == " ":
            result_html += text
        elif flag == "+":
            result_html += f"<ins>{text}</ins>"
        elif flag:
            result_html += f"<del>{text}</del>"

    return result_html


def html_diff_to_markdown(txt):
    r = txt.replace("<ins>", " **[+")  # 留个空格 否则markdown解析容易出错
    r = r.replace("</ins>", "+]** ")
    r = r.replace("<del>", " **[-")
    r = r.replace("</del>", "-]** ")
    return r


def shorten(s, length):
    return s if len(s) < length else (s[:length] + "...")


def html_to_text(html):
    return BeautifulSoup(html, 'html.parser').get_text()


if __name__ == '__main__':
    old = "【全部公告本科生院 研究生院关于2020-2021学年秋冬学期课程调整安排的通知】 各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："
    new = "【全部公告研究生院、本科生院 关于2020-2021学年秋冬学期课程调整安排的通知】 各学院（系），行政各部门，各校区管委会，直属各单位，各任课教师、各位同学："

    r1 = html_diff(old, new)
    r2 = html_diff2(old, new)
    r3 = html_diff_to_markdown(r1)
    r4 = html_diff_to_markdown(r2)

    print(old)
    print(new)
    print(r1)
    print(r2)
    print(r3)
    print(r4)

# print(diff_result)
