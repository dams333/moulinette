FROM python:3.13-rc-bullseye

RUN mkdir -p /tmp/subject
RUN mkdir -p /tmp/rendu
RUN mkdir -p /tmp/traces

RUN mkdir -p /usr/client
COPY ./srcs /usr/client
WORKDIR /usr/client

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "client.py"]