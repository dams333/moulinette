FROM python:3.13-rc-bullseye

RUN apt-get update
RUN apt-get install -y gcc llvm-11 clang-11

RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install norminette

RUN useradd -ms /bin/bash codemachine
RUN passwd -d codemachine
RUN mkdir -p /codemachine

RUN mkdir -p /usr/runner
COPY ./srcs /usr/runner
WORKDIR /usr/runner

RUN pip install -r requirements.txt

RUN chmod -R 700 /usr/runner

ENTRYPOINT ["python", "codemachine.py"]