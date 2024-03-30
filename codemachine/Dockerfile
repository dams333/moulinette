FROM python:3.13-rc-bullseye

RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install norminette

RUN useradd -ms /bin/bash codemachine
RUN mkdir -p /codemachine
RUN chown codemachine:codemachine /codemachine

RUN mkdir -p /usr/runner
COPY ./srcs /usr/runner
WORKDIR /usr/runner

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "codemachine.py"]