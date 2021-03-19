FROM luminoleon/pyppeteer

LABEL maintainer="Luminoleon <luminoleon@outlook.com>"

COPY claimer.py /

CMD [ "python3", "/claimer.py" ]