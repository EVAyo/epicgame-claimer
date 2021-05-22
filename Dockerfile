FROM luminoleon/pyppeteer

LABEL maintainer="Luminoleon <luminoleon@outlook.com>"

RUN pip3 install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple schedule

COPY epicgames_claimer.py /

CMD [ "python3", "/epicgames_claimer.py" ]
