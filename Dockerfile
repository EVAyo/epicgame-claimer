FROM ubuntu

LABEL maintainer="Luminoleon <Luminoleon@outlook.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i "s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list \
    && sed -i "s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list \
    && apt update \
    && apt install -y python3 python3-pip libnss3 xvfb gconf-service libasound2 \ 
    libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 \
    libgbm1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 \
    libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation \
    libappindicator1 lsb-release xdg-utils wget \
    && pip3 install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple pyppeteer \
    && pyppeteer-install \
    && apt clean

COPY run.sh /
COPY claimer.py /
RUN chmod +x *.py && chmod +x *.sh

CMD [ "./run.sh" ]