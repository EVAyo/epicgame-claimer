FROM luminoleon/pyppeteer

LABEL maintainer="Luminoleon <luminoleon@outlook.com>"

RUN pip3 install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple schedule

COPY claimer.py /

CMD [ "python3", "/claimer.py" ]
