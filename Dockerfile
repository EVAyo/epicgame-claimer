FROM luminoleon/pyppeteer

LABEL maintainer="Luminoleon <Luminoleon@outlook.com>"

COPY claimer.py /

CMD [ "python3", "/claimer.py" ]