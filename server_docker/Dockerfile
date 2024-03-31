FROM python:3.13-rc-bullseye

RUN mkdir -p /usr/moulinette
COPY ./srcs /usr/moulinette
WORKDIR /usr/moulinette

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "moulinette.py"]