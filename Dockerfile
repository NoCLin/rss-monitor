FROM python:3.6-slim


RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list
RUN set -ex && \
    apt-get update && \
    apt-get install tzdata -yqq && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt -i https://pypi.doubanio.com/simple

WORKDIR /code


CMD python /code/main.py
