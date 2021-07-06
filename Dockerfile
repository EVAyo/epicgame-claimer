FROM ubuntu

LABEL maintainer="Luminoleon <luminoleon@outlook.com>"

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai run_at=09:00 auto_update=false

COPY requirements.txt /

RUN apt update \
    && apt install -y python3 python3-pip gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pyppeteer-install \
    && apt purge -y python3-pip \
    && apt autoremove -y \
    && apt clean

COPY *.py /

CMD [ "bash", "-c", "if ${auto_update}; then file_name='epicgames_claimer_auto_update.py'; else file_name='epicgames_claimer.py'; fi && python3 ${file_name} --run-at ${run_at}" ]
